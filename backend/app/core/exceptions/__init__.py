# backend/app/core/exceptions/__init__.py
"""Core exceptions module."""

from app.core.exceptions.handlers import (
    NotFoundError,
    register_exception_handlers,
)

__all__ = [
    "NotFoundError",
    "register_exception_handlers",
]
