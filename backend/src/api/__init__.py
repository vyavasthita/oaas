from fastapi import FastAPI
from src.api.dependencies.config_dependency import Config
from src.api.views import health
from src.observability.otel_collector.logging.otel_logging_setup import OpenTelemetryLoggingSetup
from src.observability.otel_collector.tracing.otel_tracing_setup import setup_tracing


# Initialize OpenTelemetry logging before app initialization
otel_setup = OpenTelemetryLoggingSetup(
    otlp_endpoint=Config().OTEL_EXPORTER_LOGS_ENDPOINT,
    service_name=Config().OTEL_SERVICE_NAME
)


app = FastAPI()


# Initialize OpenTelemetry tracing for FastAPI
setup_tracing(
    app,
    service_name=Config().OTEL_SERVICE_NAME,
    otlp_endpoint=Config().OTEL_EXPORTER_TRACES_ENDPOINT
)


app.include_router(health.router, tags=["Health Check"])