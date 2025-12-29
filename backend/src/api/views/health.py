from fastapi import APIRouter, Depends
import logging

router = APIRouter()

# Get a logger for this module
logger = logging.getLogger(__name__)


@router.get("/health", tags=["Health Check"])
async def health_check() -> str:
    logger.info("Health endpoint called")
    return "Hello from Tic Tac Toe"
