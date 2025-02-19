from typing import Optional
from typing import List, Union
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    # Observability
    OTEL_EXPORTER_ENDPOINT: str = ""