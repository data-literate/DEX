"""Middleware for Prometheus metrics collection."""

import time
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from dataenginex.metrics import (
    http_exceptions_total,
    http_request_duration_seconds,
    http_requests_in_flight,
    http_requests_total,
)


class PrometheusMetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect Prometheus metrics for HTTP requests."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and collect metrics."""
        # Skip metrics collection for the /metrics endpoint itself
        if request.url.path == "/metrics":
            return await call_next(request)

        method = request.method
        path = request.url.path

        # Track in-flight requests
        http_requests_in_flight.inc()

        start_time = time.time()

        try:
            # Process request
            response = await call_next(request)
            status = response.status_code

            # Record request metrics
            http_requests_total.labels(method=method, endpoint=path, status=status).inc()

            return response

        except Exception as exc:
            # Track exceptions
            http_exceptions_total.labels(exception_type=type(exc).__name__).inc()
            http_requests_total.labels(method=method, endpoint=path, status=500).inc()
            raise

        finally:
            # Record duration
            duration = time.time() - start_time
            http_request_duration_seconds.labels(method=method, endpoint=path).observe(
                duration
            )

            # Decrement in-flight counter
            http_requests_in_flight.dec()
