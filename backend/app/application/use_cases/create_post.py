# backend/app/application/use_cases/create_post.py
"""Create post use case."""

from __future__ import annotations

from typing import BinaryIO

from app.application.ports.storage_service import StoragePort
from app.application.ports.summarizer_service import SummarizerPort
from app.core.logging import get_logger
from app.domain.entities.post import Post
from app.domain.interfaces.post_repository import PostRepository

logger = get_logger(__name__)


class CreatePostUseCase:
    """Create and persist a new post."""

    def __init__(
        self,
        repository: PostRepository,
        summarizer: SummarizerPort,
        storage: StoragePort,
    ) -> None:
        self._repository = repository
        self._summarizer = summarizer
        self._storage = storage

    def execute(
        self,
        title: str,
        description: str,
        file_data: BinaryIO | None = None,
        filename: str | None = None,
    ) -> Post:
        """Create a new post."""
        title = title.strip()
        description = description.strip()

        if not title:
            raise ValueError("title cannot be empty")

        if not description:
            raise ValueError("description cannot be empty")

        file_path = None

        if file_data and filename:
            file_path = self._storage.save_file(file_data, filename)

        summary = self._summarizer.summarize(description)

        post = Post(
            title=title,
            description=description,
            summary=summary,
            file_path=file_path,
        )

        logger.info("Creating post '%s'", title)
        saved_post = self._repository.create(post)
        logger.info("Post created with id=%s", saved_post.id)

        return saved_post
