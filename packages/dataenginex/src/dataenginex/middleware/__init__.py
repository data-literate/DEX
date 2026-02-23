"""Middleware — logging, metrics, tracing, and request handling.

Public API::

    from dataenginex.middleware import (
        configure_logging, get_logger, APP_VERSION,
        get_metrics, PrometheusMetricsMiddleware,
        RequestLoggingMiddleware,
        configure_tracing, instrument_fastapi, get_tracer,
    )
"""

from __future__ import annotations

from .logging_config import APP_VERSION, configure_logging, get_logger
from .metrics import get_metrics
from .metrics_middleware import PrometheusMetricsMiddleware
from .request_logging import RequestLoggingMiddleware
from .tracing import configure_tracing, get_tracer, instrument_fastapi

__all__ = [
    # Logging
    "APP_VERSION",
    "configure_logging",
    "get_logger",
    # Metrics
    "PrometheusMetricsMiddleware",
    "get_metrics",
    # Request logging
    "RequestLoggingMiddleware",
    # Tracing
    "configure_tracing",
    "get_tracer",
    "instrument_fastapi",
]
