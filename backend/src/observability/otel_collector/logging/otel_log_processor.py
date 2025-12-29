"""
Log Processor for OpenTelemetry Collector integration.
Defines the configuration and initialization for log processors (e.g., batch, resource enrichment).
"""

from opentelemetry.sdk._logs.export import BatchLogRecordProcessor


class OTLPLogProcessor:
	"""
	Configures the log processor for OpenTelemetry logging.
	By default, uses a batch processor for efficiency.
	"""
	def __init__(self, exporter):
		# exporter: An instance of a log exporter (e.g., OTLPLogExporter)
		self.processor = BatchLogRecordProcessor(exporter)

	def get_processor(self):
		"""
		Returns the configured log processor instance.
		"""
		return self.processor
