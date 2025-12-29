"""
logging.py

Centralized logging setup for the backend application.

Features:
- Configures structured JSON logging for compatibility with Loki (and other log aggregators).
- Can be imported and used across the app for consistent, structured logging.
- Easy to extend for tracing, metrics, or other observability needs.


Usage Example:
    from observability.logging import setup_logging
    setup_logging()
    import logging
    logger = logging.getLogger("my_module")
    logger.info("User logged in", extra={"user_id": 123})

This will emit logs in JSON format to stdout, which can be scraped by Loki.
"""

import logging
import sys
import json


class JsonFormatter(logging.Formatter):
    """
    Formats log records as JSON for Loki ingestion.

    Each log record is output as a JSON object with keys:
        - level: Log level (e.g., INFO, ERROR)
        - logger: Logger name
        - message: Log message
        - time: Timestamp (ISO8601)
        - exception: (optional) Exception traceback if present

    Example output:
        {"level": "INFO", "logger": "my_module", "message": "User logged in", "time": "2025-12-29 12:34:56"}
    """
    def format(self, record):
        # Build a dictionary for the log record
        log_record = {
            'level': record.levelname,  # Log level (e.g., INFO, ERROR)
            'logger': record.name,      # Logger name
            'message': record.getMessage(),  # The log message
            'time': self.formatTime(record, self.datefmt),  # Timestamp
        }
        # If there is exception info, add it to the log record
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        # Convert the dictionary to a JSON string
        return json.dumps(log_record)


def setup_logging(level=logging.INFO):
    """
    Sets up the root logger to output JSON logs to stdout.

    Args:
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG)

    Call this function early in your app (e.g., at startup) to ensure all logs are structured and go to stdout.

    Example:
        setup_logging(logging.DEBUG)
        logger = logging.getLogger("api")
        logger.info("API started", extra={"version": "1.0.0"})
    """
    handler = logging.StreamHandler(sys.stdout)  # Output logs to stdout
    handler.setFormatter(JsonFormatter())        # Use our JSON formatter
    root_logger = logging.getLogger()            # Get the root logger
    root_logger.setLevel(level)                  # Set the log level
    root_logger.handlers = [handler]             # Replace handlers with our handler
    root_logger.propagate = False                # Prevent double logging
