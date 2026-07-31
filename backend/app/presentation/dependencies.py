# backend/app/presentation/dependencies.py
from __future__ import annotations

from collections.abc import Generator
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.ports.summarizer_service import SummarizerPort
from app.domain.interfaces.post_repository import PostRepository
from app.infrastructure.database.session import get_session_factory
from app.infrastructure.repositories.post_repository import SqlAlchemyPostRepository
from app.infrastructure.services.summarizer_service import LexicalSummarizerService


@lru_cache(maxsize=1)
def get_summarizer_service() -> SummarizerPort:
    """Return the singleton summarizer service."""
    return LexicalSummarizerService()


def get_db_session() -> Generator[Session]:
    """
    Yield a SQLAlchemy session.

    Transaction management is handled by the repository layer.
    This dependency is only responsible for opening and closing
    the session.
    """

    session = get_session_factory()()

    try:
        yield session
    finally:
        session.close()


def get_post_repository(
    session: Session = Depends(get_db_session),
) -> PostRepository:
    """Return the repository bound to the current request session."""

    return SqlAlchemyPostRepository(session)
