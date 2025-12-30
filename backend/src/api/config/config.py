from typing import Optional
from typing import List, Union
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    # Observability
    OTEL_EXPORTER_LOGS_ENDPOINT: str = ""  # OTLP endpoint for logs
    OTEL_EXPORTER_TRACES_ENDPOINT: str = ""  # OTLP endpoint for traces
    OTEL_EXPORTER_METRICS_ENDPOINT: str = ""  # OTLP endpoint for metrics
    OTEL_SERVICE_NAME: str = "tic-tac-toe-backend"  # Service name for OTel resources
    RATE_LIMITED_LOG_INTERVAL_SECONDS: int = 60  # Interval for rate-limited logging
