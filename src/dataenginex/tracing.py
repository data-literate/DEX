"""OpenTelemetry tracing configuration for DataEngineX."""

import os

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from dataenginex.logging_config import APP_NAME, APP_VERSION


def configure_tracing(
    service_name: str = APP_NAME,
    service_version: str = APP_VERSION,
    otlp_endpoint: str | None = None,
    enable_console_export: bool = False,
) -> TracerProvider:
    """
    Configure OpenTelemetry tracing.

    Args:
        service_name: Name of the service
        service_version: Version of the service
        otlp_endpoint: OTLP collector endpoint (e.g., "http://localhost:4317")
        enable_console_export: If True, print spans to console (for debugging)

    Returns:
        Configured TracerProvider
    """
    # Create resource with service information
    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": service_version,
            "deployment.environment": os.getenv("ENVIRONMENT", "dev"),
        }
    )

    # Create tracer provider
    provider = TracerProvider(resource=resource)

    # Add span processors
    if otlp_endpoint:
        # Export to OTLP collector (Jaeger, Tempo, etc.)
        # Remove http:// or https:// prefix for gRPC endpoint
        endpoint = otlp_endpoint.replace("http://", "").replace("https://", "")
        otlp_exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    if enable_console_export:
        # Export to console for debugging
        console_exporter = ConsoleSpanExporter()
        provider.add_span_processor(BatchSpanProcessor(console_exporter))

    # Set as global tracer provider
    trace.set_tracer_provider(provider)

    return provider


def instrument_fastapi(app: FastAPI) -> None:
    """
    Instrument FastAPI application with OpenTelemetry.

    Args:
        app: FastAPI application instance
    """
    FastAPIInstrumentor.instrument_app(app)


def get_tracer(name: str) -> trace.Tracer:
    """
    Get a tracer instance.

    Args:
        name: Tracer name (typically __name__ of the calling module)

    Returns:
        Tracer instance
    """
    return trace.get_tracer(name)
