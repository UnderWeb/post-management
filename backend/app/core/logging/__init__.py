# backend/app/core/logging/__init__.py
"""Core logging module."""

from app.core.logging.logger import (
    get_logger,
    setup_logging,
)

__all__ = [
    "get_logger",
    "setup_logging",
]
