"""
OpenTelemetry Logging Setup for FastAPI Application.
Initializes the OTLP log receiver, processor, and exporter, and attaches them to the Python logging system.
"""
import logging
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import get_logger
try:
    from opentelemetry.sdk._logs import set_log_emitter_provider
except ImportError:
    set_log_emitter_provider = None
try:
    from opentelemetry.sdk._logs import set_logger_provider
except ImportError:
    set_logger_provider = None
from src.api.observability.otel_collector.logging.otel_log_exporter import OTLPLogExporterWrapper
from src.api.observability.otel_collector.logging.otel_log_processor import OTLPLogProcessor


class OpenTelemetryLoggingSetup:
    """
    Sets up OpenTelemetry logging for the application.
    This class wires together the exporter, processor, and logger provider.
    """
    def __init__(self, otlp_endpoint: str = "http://otel-collector:4318/v1/logs"):
        # Initialize the OTLP log exporter
        self.exporter_wrapper = OTLPLogExporterWrapper(endpoint=otlp_endpoint)
        
        # Initialize the log processor with the exporter
        self.processor = OTLPLogProcessor(self.exporter_wrapper.get_exporter()).get_processor()
        
        # Set up the logger provider and add the processor
        self.logger_provider = LoggerProvider()
        self.logger_provider.add_log_record_processor(self.processor)
        # For OpenTelemetry >=1.17, set the log emitter provider
        if set_log_emitter_provider:
            set_log_emitter_provider(self.logger_provider)
        elif set_logger_provider:
            set_logger_provider(self.logger_provider)
        
        # Optionally, attach the OpenTelemetry logger to the Python logging system
        self.attach_to_python_logging()

    def attach_to_python_logging(self):
        """
        Optionally attach the OpenTelemetry logger to the root Python logger.
        This allows standard logging calls to be exported via OpenTelemetry.
        """
        logging.basicConfig(level=logging.INFO)
        # You can further customize handlers/formatters here if needed.
