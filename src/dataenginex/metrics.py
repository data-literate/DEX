"""Prometheus metrics configuration for DataEngineX."""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import REGISTRY

# Request metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

http_requests_in_flight = Gauge(
    "http_requests_in_flight",
    "Number of HTTP requests currently being processed",
)

http_exceptions_total = Counter(
    "http_exceptions_total",
    "Total HTTP exceptions",
    ["exception_type"],
)


def get_metrics() -> tuple[bytes, str]:
    """
    Generate Prometheus metrics in text format.

    Returns:
        Tuple of (metrics_data, content_type)
    """
    return generate_latest(REGISTRY), CONTENT_TYPE_LATEST
