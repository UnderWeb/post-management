# backend/app/presentation/dependencies.py
"""Dependency injection providers for the presentation layer."""

from __future__ import annotations

from collections.abc import Generator
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.ports.storage_service import StoragePort
from app.application.ports.summarizer_service import SummarizerPort
from app.domain.interfaces.post_repository import PostRepository
from app.infrastructure.database.session import get_session_factory
from app.infrastructure.repositories.post_repository import SqlAlchemyPostRepository
from app.infrastructure.services.s3_storage_service import S3StorageService
from app.infrastructure.services.summarizer_service import LexicalSummarizerService


@lru_cache(maxsize=1)
def get_summarizer_service() -> SummarizerPort:
    """Return the singleton summarizer service."""
    return LexicalSummarizerService()


@lru_cache(maxsize=1)
def get_storage_service() -> StoragePort:
    """Return the singleton storage service."""
    return S3StorageService()


def get_db_session() -> Generator[Session]:
    """
    Provide a database session per request.

    Commits successful transactions and rolls back failed ones.
    """
    session = get_session_factory()()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_post_repository(
    session: Session = Depends(get_db_session),
) -> PostRepository:
    """Return repository bound to current request session."""
    return SqlAlchemyPostRepository(session)
