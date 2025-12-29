from functools import lru_cache
from src.api.config.config import Settings


@lru_cache
def Config():
    return Settings()