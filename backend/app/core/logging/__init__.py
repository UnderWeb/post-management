# backend/app/core/logging/__init__.py
from app.core.logging.logger import (
    get_logger,
    setup_logging,
)

__all__ = [
    "setup_logging",
    "get_logger",
]
