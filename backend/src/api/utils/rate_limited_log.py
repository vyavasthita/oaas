import time
import functools


def rate_limited_log(interval_seconds: int = 60):
    """
    Decorator to rate-limit logging actions inside an async endpoint or function.
    Usage:
        @rate_limited_log(interval_seconds=60)
        async def endpoint(...):
            logger.info("message")  # Only logs if interval has passed
    """
    def decorator(func):
        last_logged = [0.0]
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            wrapper._can_log = False
            now = time.time()
            if now - last_logged[0] > interval_seconds:
                wrapper._can_log = True
                last_logged[0] = now
            return await func(*args, **kwargs)
        wrapper._can_log = True
        return wrapper
    return decorator