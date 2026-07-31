# backend/app/application/use_cases/delete_post.py
from __future__ import annotations

from app.core.exceptions import NotFoundError
from app.core.logging import get_logger
from app.domain.interfaces.post_repository import PostRepository

logger = get_logger(__name__)


class DeletePostUseCase:
    """Delete a post."""

    def __init__(self, repository: PostRepository) -> None:
        self._repository = repository

    def execute(self, post_id: int) -> bool:
        """Delete a post by its identifier."""

        post = self._repository.get_by_id(post_id)

        if post is None:
            logger.warning("Post %s not found", post_id)
            raise NotFoundError("Post", post_id)

        deleted = self._repository.delete(post_id)

        logger.info("Post %s deleted", post_id)

        return deleted
