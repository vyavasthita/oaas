import time
import functools
import logging


def rate_limited_log(interval_seconds: int = 60):
    """
    Decorator to rate-limit logging actions inside an endpoint or function.
    Usage:
        @rate_limited_log(interval_seconds=60)
        def endpoint(...):
            logger.info("message")  # Only logs if interval has passed
    """
    def decorator(func):
        last_logged = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_logged[0] > interval_seconds:
                wrapper._can_log = True
                last_logged[0] = now
            else:
                wrapper._can_log = False
            return func(*args, **kwargs)
        wrapper._can_log = True
        return wrapper
    return decorator
