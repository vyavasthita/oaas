"""
OTLP Log Exporter for OpenTelemetry Collector integration.
Defines the configuration and initialization for the OTLP log exporter.
"""

from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter


class OTLPLogExporterWrapper:
	"""
	Configures the OTLP log exporter to send logs to the OpenTelemetry Collector.
	"""
	def __init__(self, endpoint: str):
		# endpoint: The OTLP HTTP endpoint for the Collector
		self.exporter = OTLPLogExporter(endpoint=endpoint)

	def get_exporter(self):
		"""
		Returns the configured OTLP log exporter instance.
		"""
		return self.exporter
