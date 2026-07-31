# backend/app/core/logging/logger.py
from __future__ import annotations

import logging
import sys
from typing import Any


class KeyValueFormatter(logging.Formatter):
    """Structured key-value log formatter."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)

        return " | ".join(
            f"{key}={value}"
            for key, value in log_entry.items()
        )


def setup_logging(level: str = "INFO") -> None:
    """Configure application-wide structured logging."""

    root_logger = logging.getLogger()
    root_logger.setLevel(
        getattr(logging, level.upper(), logging.INFO)
    )

    handler = logging.StreamHandler(sys.stdout)

    formatter = KeyValueFormatter(
        datefmt="%Y-%m-%dT%H:%M:%S"
    )

    handler.setFormatter(formatter)

    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(
        logging.WARNING
    )

    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.WARNING
    )


def get_logger(name: str) -> logging.Logger:
    """Return a named logger instance."""

    return logging.getLogger(name)
