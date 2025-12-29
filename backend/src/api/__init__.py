from fastapi import FastAPI
from src.api.dependencies.config_dependency import Config
from src.observability.logging import setup_logging
from src.api.views import health

import logging

setup_logging()  # Configure logging before app initialization

app = FastAPI()

app.include_router(health.router, tags=["Health Check"])