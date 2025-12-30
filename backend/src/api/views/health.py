from fastapi import APIRouter
import logging
from src.api.utils.rate_limited_log import rate_limited_log


router = APIRouter()

# Get a logger for this module
logger = logging.getLogger(__name__)


@router.get("/health", tags=["Health Check"])
@rate_limited_log(interval_seconds=60)
async def health_check() -> str:
    if health_check._can_log:
        logger.info("Tic Tac Toe Service is healthy.")
    return "Tic Tac Toe Service is healthy."
