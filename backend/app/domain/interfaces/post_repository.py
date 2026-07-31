# backend/app/domain/interfaces/post_repository.py
from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.post import Post


class PostRepository(ABC):
    """Repository contract for Post persistence."""

    @abstractmethod
    def create(self, post: Post) -> Post:
        """Persist a post and return the created entity."""

    @abstractmethod
    def list(self) -> list[Post]:
        """Return all posts."""

    @abstractmethod
    def get_by_id(self, post_id: int) -> Post | None:
        """Return a post by identifier."""

    @abstractmethod
    def delete(self, post_id: int) -> bool:
        """Delete a post and return whether it existed."""
