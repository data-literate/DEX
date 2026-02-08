import os
from collections.abc import AsyncIterator, Mapping, Sequence
from contextlib import asynccontextmanager
from typing import Any

import structlog
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from dataenginex.errors import APIHTTPException, ServiceUnavailableError
from dataenginex.health import HealthChecker, HealthStatus
from dataenginex.logging_config import APP_VERSION, configure_logging
from dataenginex.metrics import get_metrics
from dataenginex.metrics_middleware import PrometheusMetricsMiddleware
from dataenginex.middleware import RequestLoggingMiddleware
from dataenginex.schemas import (
    ComponentStatus,
    EchoRequest,
    EchoResponse,
    ErrorDetail,
    ErrorResponse,
    HealthResponse,
    ReadinessResponse,
    RootResponse,
    StartupResponse,
)
from dataenginex.tracing import configure_tracing, instrument_fastapi

# Configure logging on startup
log_level = os.getenv("LOG_LEVEL", "INFO")
json_logs = os.getenv("LOG_FORMAT", "json") == "json"
configure_logging(log_level=log_level, json_logs=json_logs)

logger = structlog.get_logger(__name__)

# Configure tracing
otlp_endpoint = os.getenv("OTLP_ENDPOINT")  # e.g., "http://localhost:4317"
enable_console_traces = os.getenv("ENABLE_CONSOLE_TRACES", "false").lower() == "true"
configure_tracing(
    otlp_endpoint=otlp_endpoint, enable_console_export=enable_console_traces
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager."""
    app.state.startup_complete = False
    # Startup
    logger.info("application_started", environment=os.getenv("ENVIRONMENT", "dev"))
    app.state.startup_complete = True
    yield
    # Shutdown
    app.state.startup_complete = False
    logger.info("application_shutdown")


app = FastAPI(title="DataEngineX", version=APP_VERSION, lifespan=lifespan)

# Instrument FastAPI with OpenTelemetry
instrument_fastapi(app)

# Add middleware (order matters - outer to inner)
app.add_middleware(RequestLoggingMiddleware)  # Logging
app.add_middleware(PrometheusMetricsMiddleware)  # Metrics

health_checker = HealthChecker()


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


def _format_validation_errors(
    errors: Sequence[Mapping[str, Any]],
) -> list[ErrorDetail]:
    details: list[ErrorDetail] = []
    for error in errors:
        loc = error.get("loc", [])
        if isinstance(loc, (list, tuple)):
            field = ".".join(str(item) for item in loc if item != "body")
        else:
            field = str(loc)
        details.append(
            ErrorDetail(
                field=field or None,
                message=str(error.get("msg", "Invalid value")),
                type=str(error.get("type", "validation_error")),
            )
        )
    return details


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = _format_validation_errors(exc.errors())
    payload = ErrorResponse(
        error="validation_error",
        message="Request validation failed",
        request_id=_request_id(request),
        details=details,
    )
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    code = "http_error"
    details = None
    if isinstance(exc, APIHTTPException):
        code = exc.code
        details = exc.details
    payload = ErrorResponse(
        error=code,
        message=str(exc.detail),
        request_id=_request_id(request),
        details=details,
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("unhandled_exception", error=str(exc), error_type=type(exc).__name__)
    payload = ErrorResponse(
        error="internal_server_error",
        message="Unexpected error occurred",
        request_id=_request_id(request),
    )
    return JSONResponse(status_code=500, content=payload.model_dump())


@app.get("/metrics")
async def metrics() -> Response:
    """Prometheus metrics endpoint."""
    data, content_type = get_metrics()
    return Response(content=data, media_type=content_type)


@app.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    """Root endpoint returning API info."""
    logger.debug("root_endpoint_called")
    return RootResponse(message="DataEngineX API", version=APP_VERSION)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Liveness check endpoint."""
    logger.debug("health check")
    return HealthResponse(status="alive")


@app.get("/ready", response_model=ReadinessResponse)
async def readiness_check() -> ReadinessResponse:
    """Readiness check endpoint."""
    logger.debug("readiness_check_called")
    components = await health_checker.check_all()
    overall = health_checker.overall_status(components)
    status = "ready" if overall != HealthStatus.UNHEALTHY else "not_ready"
    if overall == HealthStatus.UNHEALTHY:
        raise ServiceUnavailableError(message="Dependencies are unhealthy")
    return ReadinessResponse(
        status=status,
        components=[ComponentStatus(**component.to_dict()) for component in components],
    )


@app.get("/startup", response_model=StartupResponse)
def startup_check() -> StartupResponse:
    """Startup probe endpoint."""
    ready = bool(getattr(app.state, "startup_complete", False))
    return StartupResponse(status="started" if ready else "starting")


@app.post("/echo", response_model=EchoResponse)
def echo_payload(payload: EchoRequest) -> EchoResponse:
    """Echo endpoint to validate request/response models."""
    return EchoResponse(
        message=payload.message,
        count=payload.count,
        echo=[payload.message for _ in range(payload.count)],
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
