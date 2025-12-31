from src.api.dependencies.config_dependency import Config
from src.api.views import health
from src.observability.otel_collector.logging.otel_logging_setup import OpenTelemetryLoggingSetup
from src.observability.otel_collector.tracing.otel_tracing_setup import OpenTelemetryTracingSetup
from src.observability.otel_collector.metrics.otel_metrics_setup import OpenTelemetryMetricsSetup
from src.observability.otel_collector.metrics.metrics_middleware import MetricsMiddleware


class AppInitializer:
    """
    Orchestrates all OpenTelemetry and FastAPI initialization steps for the backend application.
    Handles logging, tracing, metrics, middleware, and router registration in a modular way.
    """

    def setup_otel_logging(self):
        """
        Set up OpenTelemetry logging for the application.
        Initializes the OTLP log exporter, processor, and logger provider.
        """
        # Create and configure the OpenTelemetry logging setup
        otel_logging = OpenTelemetryLoggingSetup(
            otlp_endpoint=Config().OTEL_EXPORTER_LOGS_ENDPOINT,
            service_name=Config().OTEL_SERVICE_NAME
        )

        # Initialize logging
        otel_logging.setup_logging()

    def setup_otel_tracing(self, app):
        """
        Set up OpenTelemetry tracing for FastAPI.
        Initializes the tracer provider and instruments the FastAPI app.
        """
        # Create and configure the OpenTelemetry tracing setup
        otel_tracing = OpenTelemetryTracingSetup(
            app,
            service_name=Config().OTEL_SERVICE_NAME,
            otlp_endpoint=Config().OTEL_EXPORTER_TRACES_ENDPOINT
        )

        # Initialize tracing
        otel_tracing.setup_tracing()

        # Instrument FastAPI for tracing
        otel_tracing.instrument_fastapi()

    def setup_otel_metrics(self, app):
        """
        Set up OpenTelemetry metrics for FastAPI.
        Initializes the metrics provider and instruments the FastAPI app.
        Returns the meter instance for custom metrics.
        """
        # Create and configure the OpenTelemetry metrics setup
        otel_metrics = OpenTelemetryMetricsSetup(
            app,
            service_name=Config().OTEL_SERVICE_NAME,
            otlp_endpoint=Config().OTEL_EXPORTER_METRICS_ENDPOINT
        )

        # Initialize metrics
        otel_metrics.setup()

        # Instrument FastAPI for metrics
        otel_metrics.instrument_fastapi()

        # Return the meter for custom metrics
        return otel_metrics.get_meter()

    def add_metrics_middleware(self, app, meter):
        """
        Add MetricsMiddleware to the FastAPI app for HTTP request metrics.
        """
        # Add the custom metrics middleware to the app
        app.add_middleware(MetricsMiddleware, meter=meter)

    def add_middlewares(self, app, meter):
        """
        Add all common middlewares to the FastAPI app.
        Extend this method to add more middlewares as needed.
        """
        # Add metrics middleware (extend here for more middlewares)
        self.add_metrics_middleware(app, meter)

    def register_routers(self, app):
        """
        Register all FastAPI routers for the application.
        Add new routers here as the API grows.
        """
        # Register health check router
        app.include_router(health.router, tags=["Health Check"])

    def pre_initialization(self):
        """
        Perform all setup steps that must occur before FastAPI app instantiation.
        """
        # Set up logging before app instantiation
        self.setup_otel_logging()

    def post_initialization(self, app):
        """
        Perform all setup steps that require the FastAPI app instance.
        """
        # Set up tracing after app instantiation
        self.setup_otel_tracing(app)

        # Set up metrics and get the meter
        meter = self.setup_otel_metrics(app)

        # Add all middlewares
        self.add_middlewares(app, meter)

        # Register all routers
        self.register_routers(app)
