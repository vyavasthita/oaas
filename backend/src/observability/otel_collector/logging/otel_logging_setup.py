"""
OpenTelemetry Logging Setup for FastAPI Application.
Initializes the OTLP log receiver, processor, and exporter, and attaches them to the Python logging system.
"""
import logging
import atexit
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider
from src.observability.otel_collector.logging.otel_log_exporter import OTLPLogExporterWrapper
from src.observability.otel_collector.logging.otel_log_processor import OTLPLogProcessor


class OpenTelemetryLoggingSetup:
	"""
	Sets up OpenTelemetry logging for the application.
	This class wires together the exporter, processor, and logger provider.
	"""
	def __init__(self, otlp_endpoint: str, service_name: str):
		self.otlp_endpoint = otlp_endpoint
		self.service_name = service_name

	def setup_logging(self):
		# Initialize the OTLP log exporter
		self.exporter_wrapper = OTLPLogExporterWrapper(endpoint=self.otlp_endpoint)
		
		# Initialize the log processor with the exporter
		self.processor = OTLPLogProcessor(self.exporter_wrapper.get_exporter()).get_processor()
		
		# Set up the logger provider and add the processor
		self.logger_provider = LoggerProvider(
			resource=Resource.create({"service.name": self.service_name})
		)
		
		self.logger_provider.add_log_record_processor(self.processor)
		set_logger_provider(self.logger_provider)
		
		# Optionally, attach the OpenTelemetry logger to the Python logging system
		self.attach_to_python_logging()
		
		# Ensure logs are flushed on shutdown
		atexit.register(self.shutdown)

	def shutdown(self):
		try:
			self.logger_provider.shutdown()
		except Exception as e:
			logging.error(f"OTEL logger provider shutdown error: {e}")

	def attach_to_python_logging(self):
		"""
		Attach the OpenTelemetry LoggingHandler to the root Python logger.
		This ensures all standard logging calls are exported as OTEL logs with resource labels.
		
		The LoggingHandler intercepts standard Python log records and
		converts them to OpenTelemetry log records, 
		which are then exported in the OTEL log format.
		"""
		handler = LoggingHandler(level=logging.INFO, logger_provider=self.logger_provider)
        
		root_logger = logging.getLogger()
		root_logger.addHandler(handler)
		root_logger.setLevel(logging.INFO)
		root_logger.propagate = True
