from prometheus_client import make_asgi_app
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader


class OpenTelemetryMetricsSetup:
    def __init__(self, app, service_name: str, otlp_endpoint: str):
        self.app = app
        self.service_name = service_name
        self.otlp_endpoint = otlp_endpoint
        self.meter_provider = None
        self.prom_reader = None

    def setup(self):
        resource = Resource(attributes={SERVICE_NAME: self.service_name})

        # OTLP exporter (already working)
        otlp_exporter = OTLPMetricExporter(endpoint=self.otlp_endpoint)
        otlp_reader = PeriodicExportingMetricReader(otlp_exporter)

        self.prom_reader = PrometheusMetricReader()

        provider = MeterProvider(
            resource=resource,
            metric_readers=[otlp_reader, self.prom_reader],
        )

        self.meter_provider = provider

        # Expose /metrics endpoint manually using prometheus_client
        self.app.mount("/metrics", make_asgi_app())

    def instrument_fastapi(self):
        FastAPIInstrumentor.instrument_app(
            self.app,
            meter_provider=self.meter_provider,
        )

    def get_meter(self):
        if not self.meter_provider:
            raise RuntimeError("MeterProvider not initialized. Call setup() first.")
        return self.meter_provider.get_meter(self.service_name)
