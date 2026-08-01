# backend/app/application/use_cases/delete_post.py
"""Delete post use case."""

from __future__ import annotations

from app.application.ports.storage_service import StoragePort
from app.core.exceptions import NotFoundError
from app.core.logging import get_logger
from app.domain.interfaces.post_repository import PostRepository

logger = get_logger(__name__)


class DeletePostUseCase:
    """Delete a post and its associated file."""

    def __init__(
        self,
        repository: PostRepository,
        storage: StoragePort,
    ) -> None:
        self._repository = repository
        self._storage = storage

    def execute(self, post_id: int) -> bool:
        """Delete a post by its identifier and remove associated file."""

        post = self._repository.get_by_id(post_id)

        if post is None:
            logger.warning("Post %s not found", post_id)
            raise NotFoundError("Post", post_id)

        if post.file_path:
            try:
                self._storage.delete_file(post.file_path)
                logger.info(
                    "Deleted file %s for post %s",
                    post.file_path,
                    post_id,
                )
            except Exception as exc:
                logger.error(
                    "Failed to delete file %s: %s",
                    post.file_path,
                    exc,
                )

        deleted = self._repository.delete(post_id)
        logger.info("Post %s deleted", post_id)

        return deleted
