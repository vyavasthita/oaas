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


def setup_tracing(app, service_name, otlp_endpoint):
    """
    Sets up OpenTelemetry tracing for a FastAPI app.
    - Adds OTLP exporter, batch processor, and resource attributes.
    - Instruments FastAPI for automatic tracing.
    """
    resource = Resource.create({"service.name": service_name})
    tracer_provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(
        endpoint=otlp_endpoint,
        # OTLPSpanExporter expects /v1/traces endpoint for HTTP
        # If using HTTP, ensure the endpoint ends with /v1/traces
    )
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
    logging.info("OpenTelemetry tracing is set up for FastAPI.")
