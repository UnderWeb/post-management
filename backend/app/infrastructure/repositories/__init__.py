# backend/app/infrastructure/repositories/__init__.py
from app.infrastructure.repositories.post_repository import (
    SqlAlchemyPostRepository,
)

__all__ = [
    "SqlAlchemyPostRepository",
]
