# backend/app/infrastructure/database/models/base.py
"""Base declarative model."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""
