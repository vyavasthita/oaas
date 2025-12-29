from fastapi import FastAPI
from src.api.dependencies.config_dependency import Config
from src.api.views import health
from src.observability.otel_collector.logging.otel_logging_setup import OpenTelemetryLoggingSetup


# Initialize OpenTelemetry logging before app initialization
otel_setup = OpenTelemetryLoggingSetup()


app = FastAPI()


app.include_router(health.router, tags=["Health Check"])