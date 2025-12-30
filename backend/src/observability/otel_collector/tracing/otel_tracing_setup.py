"""
OpenTelemetry Tracing Setup for FastAPI Application.
Initializes the OTLP trace exporter, processor, and tracer provider, and attaches them to FastAPI via middleware.
"""
import logging
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


class OpenTelemetryTracingSetup:
    """
    OpenTelemetry Tracing Setup for FastAPI Application.
    Initializes the OTLP trace exporter, processor, and tracer provider, and attaches them to FastAPI via middleware.
    """
    def __init__(self, app, service_name, otlp_endpoint):
        self.app = app
        self.service_name = service_name
        self.otlp_endpoint = otlp_endpoint

    def setup_tracing(self):
        resource = Resource.create({"service.name": self.service_name})
        tracer_provider = TracerProvider(resource=resource)
        otlp_exporter = OTLPSpanExporter(
            endpoint=self.otlp_endpoint,
        )
        span_processor = BatchSpanProcessor(otlp_exporter)
        tracer_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(tracer_provider)
        self.tracer_provider = tracer_provider
        
    def instrument_fastapi(self):
        FastAPIInstrumentor.instrument_app(self.app, tracer_provider=self.tracer_provider)
        logging.info("OpenTelemetry tracing is set up for FastAPI.")
