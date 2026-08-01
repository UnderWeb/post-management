# backend/app/infrastructure/repositories/__init__.py
"""Repositories module."""

from app.infrastructure.repositories.post_repository import (
    SqlAlchemyPostRepository,
)

__all__ = [
    "SqlAlchemyPostRepository",
]
