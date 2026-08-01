# backend/app/infrastructure/database/models/__init__.py
"""Database models module."""

from app.infrastructure.database.models.base import Base
from app.infrastructure.database.models.post_model import PostModel

__all__ = [
    "Base",
    "PostModel",
]
