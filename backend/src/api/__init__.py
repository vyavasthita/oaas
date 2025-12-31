"""
FastAPI application initialization with modular OpenTelemetry observability setup.

This file wires together logging, tracing, and metrics instrumentation for the backend,
using dedicated setup functions for maintainability and clarity.
All configuration is loaded from the central Config class for future Kubernetes compatibility.
"""

from fastapi import FastAPI
from src.api.app_initializer import AppInitializer


# Pre-initialization steps
initializer = AppInitializer()

# Pre-initialization steps
initializer.pre_initialization()

# Create FastAPI application instance
app = FastAPI()

# Post-initialization steps
initializer.post_initialization(app)