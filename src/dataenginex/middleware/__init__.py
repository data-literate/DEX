"""
Middleware - logging, metrics, tracing, and request handling.
"""

from .logging_config import APP_VERSION, configure_logging  # noqa: F401
from .metrics import get_metrics  # noqa: F401
from .metrics_middleware import PrometheusMetricsMiddleware  # noqa: F401
from .request_logging import RequestLoggingMiddleware  # noqa: F401
from .tracing import configure_tracing, instrument_fastapi  # noqa: F401

__all__ = [
    "configure_logging",
    "APP_VERSION",
    "get_metrics",
    "PrometheusMetricsMiddleware",
    "RequestLoggingMiddleware",
    "configure_tracing",
    "instrument_fastapi",
]
