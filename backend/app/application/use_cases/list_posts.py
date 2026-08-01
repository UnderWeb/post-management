# backend/app/application/use_cases/list_posts.py
"""List posts use case."""

from __future__ import annotations

from app.domain.entities.post import Post
from app.domain.interfaces.post_repository import PostRepository


class ListPostsUseCase:
    """Retrieve all posts."""

    def __init__(
        self,
        repository: PostRepository,
    ) -> None:
        self._repository = repository

    def execute(self) -> list[Post]:
        """Return all persisted posts."""

        return self._repository.list()
