# backend/app/application/use_cases/create_post.py
from __future__ import annotations

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
    ) -> None:
        self._repository = repository
        self._summarizer = summarizer

    def execute(
        self,
        nombre: str,
        descripcion: str,
    ) -> Post:
        """Create a new post."""

        nombre = nombre.strip()
        descripcion = descripcion.strip()

        if not nombre:
            raise ValueError("nombre must not be empty")

        if not descripcion:
            raise ValueError("descripcion must not be empty")

        resumen = self._summarizer.summarize(descripcion)

        post = Post(
            nombre=nombre,
            descripcion=descripcion,
            resumen=resumen,
        )

        logger.info("Creating post '%s'", nombre)

        saved_post = self._repository.create(post)

        logger.info("Post created with id=%s", saved_post.id)

        return saved_post
