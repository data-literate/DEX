import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

from dataenginex.health import HealthChecker, HealthStatus
from dataenginex.logging_config import APP_VERSION, configure_logging
from dataenginex.metrics import get_metrics
from dataenginex.metrics_middleware import PrometheusMetricsMiddleware
from dataenginex.middleware import RequestLoggingMiddleware
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


@app.get("/metrics")
async def metrics() -> Response:
    """Prometheus metrics endpoint."""
    data, content_type = get_metrics()
    return Response(content=data, media_type=content_type)


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint returning API info."""
    logger.debug("root_endpoint_called")
    return {"message": "DataEngineX API", "version": APP_VERSION}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Liveness check endpoint."""
    logger.debug("health check")
    return {"status": "alive"}


@app.get("/ready")
async def readiness_check() -> JSONResponse:
    """Readiness check endpoint."""
    logger.debug("readiness_check_called")
    components = await health_checker.check_all()
    overall = health_checker.overall_status(components)
    status_code = 200 if overall != HealthStatus.UNHEALTHY else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ready" if status_code == 200 else "not_ready",
            "components": [component.to_dict() for component in components],
        },
    )


@app.get("/startup")
def startup_check() -> dict[str, str]:
    """Startup probe endpoint."""
    ready = bool(getattr(app.state, "startup_complete", False))
    return {"status": "started" if ready else "starting"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
