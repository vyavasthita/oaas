
"""
FastAPI application initialization with modular OpenTelemetry observability setup.

This file wires together logging, tracing, and metrics instrumentation for the backend,
using dedicated setup functions for maintainability and clarity.
All configuration is loaded from the central Config class for future Kubernetes compatibility.
"""

from fastapi import FastAPI
from src.api.dependencies.config_dependency import Config
from src.api.views import health
from src.observability.otel_collector.logging.otel_logging_setup import OpenTelemetryLoggingSetup
from src.observability.otel_collector.tracing.otel_tracing_setup import OpenTelemetryTracingSetup
from src.observability.otel_collector.metrics.otel_metrics_setup import OpenTelemetryMetricsSetup


def setup_otel_logging():
    """
    Set up OpenTelemetry logging for the application.
    Initializes the OTLP log exporter, processor, and logger provider.
    """
    otel_logging = OpenTelemetryLoggingSetup(
        otlp_endpoint=Config().OTEL_EXPORTER_LOGS_ENDPOINT,
        service_name=Config().OTEL_SERVICE_NAME
    )
    otel_logging.setup_logging()

def setup_otel_tracing(app):
    """
    Set up OpenTelemetry tracing for FastAPI.
    Initializes the tracer provider and instruments the FastAPI app.
    """
    otel_tracing = OpenTelemetryTracingSetup(
        app,
        service_name=Config().OTEL_SERVICE_NAME,
        otlp_endpoint=Config().OTEL_EXPORTER_TRACES_ENDPOINT
    )
    otel_tracing.setup_tracing()
    otel_tracing.instrument_fastapi()

def setup_otel_metrics(app):
    """
    Set up OpenTelemetry metrics for FastAPI.
    Initializes the metrics provider and instruments the FastAPI app.
    """
    otel_metrics = OpenTelemetryMetricsSetup(
        app,
        service_name=Config().OTEL_SERVICE_NAME,
        otlp_endpoint=Config().OTEL_EXPORTER_METRICS_ENDPOINT
    )
    otel_metrics.setup()
    otel_metrics.instrument_fastapi()

def register_routers(app: FastAPI):
    """
    Register all FastAPI routers for the application.
    Add new routers here as the API grows.
    """
    # Register health check router
    app.include_router(health.router, tags=["Health Check"])

# Initialize OpenTelemetry logging before FastAPI app creation
setup_otel_logging()  # Logging setup must occur before app instantiation

# Create FastAPI application instance
app = FastAPI()

# Instrument FastAPI app for tracing and metrics
setup_otel_tracing(app)  # Tracing setup wires OTLP exporter and FastAPI instrumentation
setup_otel_metrics(app)  # Metrics setup wires OTLP exporter and FastAPI instrumentation

# Register all routers for the FastAPI app
register_routers(app)  # Add new routers in register_routers as needed