# backend/app/infrastructure/repositories/post_repository.py
"""Post repository implementation."""

from __future__ import annotations

import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.post import Post
from app.domain.interfaces.post_repository import PostRepository
from app.infrastructure.database.models.post_model import PostModel


class SqlAlchemyPostRepository(PostRepository):
    """SQLAlchemy implementation of PostRepository."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, post: Post) -> Post:
        """Persist a post and return the created entity."""
        return self.add(post)

    def list(self) -> list[Post]:
        """Return all posts."""
        return self.get_all()

    def add(self, post: Post) -> Post:
        """Add a new post to the database."""
        model = PostModel(
            title=post.title,
            description=post.description,
            summary=json.dumps(
                post.summary,
                ensure_ascii=False,
            ),
            file_path=post.file_path,
            created_at=post.created_at,
        )

        self.session.add(model)
        self.session.flush()

        return self._to_entity(model)

    def get_all(self) -> list[Post]:
        """Retrieve all posts from the database."""
        result = self.session.execute(select(PostModel))

        return [self._to_entity(item) for item in result.scalars().all()]

    def get_by_id(
        self,
        post_id: int,
    ) -> Post | None:
        """Retrieve a post by its identifier."""
        model = self.session.get(
            PostModel,
            post_id,
        )

        if model is None:
            return None

        return self._to_entity(model)

    def delete(
        self,
        post_id: int,
    ) -> bool:
        """Delete a post by its identifier."""
        model = self.session.get(
            PostModel,
            post_id,
        )

        if model is None:
            return False

        self.session.delete(model)

        return True

    @staticmethod
    def _to_entity(
        model: PostModel,
    ) -> Post:
        """Convert an ORM model to a domain entity."""
        summary = model.summary

        if isinstance(summary, str):
            try:
                summary = json.loads(summary)
            except json.JSONDecodeError:
                pass

        return Post(
            id=model.id,
            title=model.title,
            description=model.description,
            summary=summary,
            file_path=model.file_path,
            created_at=model.created_at,
        )
