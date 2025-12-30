from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


class OpenTelemetryMetricsSetup:
    """
    OpenTelemetry Metrics Setup for FastAPI Application.
    Initializes the OTLP metrics exporter, reader, and meter provider, and attaches them to FastAPI via instrumentation.
    """
    def __init__(self, app, service_name: str, otlp_endpoint: str):
        self.app = app
        self.service_name = service_name
        self.otlp_endpoint = otlp_endpoint

    def setup(self):
        resource = Resource(attributes={SERVICE_NAME: self.service_name})
        exporter = OTLPMetricExporter(endpoint=self.otlp_endpoint)
        reader = PeriodicExportingMetricReader(exporter)
        provider = MeterProvider(resource=resource, metric_readers=[reader])
        self.meter_provider = provider

    def instrument_fastapi(self):
        FastAPIInstrumentor().instrument_app(self.app, meter_provider=self.meter_provider)
