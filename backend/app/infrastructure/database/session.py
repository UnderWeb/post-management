# backend/app/infrastructure/database/session.py
"""Database session and engine configuration."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings

settings = Settings()

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_engine():
    """Return SQLAlchemy engine."""
    return engine


def get_session_factory() -> sessionmaker[Session]:
    """Return configured session factory."""
    return SessionLocal
