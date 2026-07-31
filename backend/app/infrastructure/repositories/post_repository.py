# backend/app/infrastructure/repositories/post_repository.py
from __future__ import annotations

import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.post import Post
from app.domain.interfaces.post_repository import PostRepository
from app.infrastructure.database.models.post_model import PostModel


class SqlAlchemyPostRepository(PostRepository):
    """SQLAlchemy implementation of the PostRepository interface."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, post: Post) -> Post:
        """Persist a new post and return the saved domain entity."""

        model = PostModel(
            nombre=post.nombre,
            descripcion=post.descripcion,
            resumen=json.dumps(post.resumen, ensure_ascii=False),
            fecha_creacion=post.fecha_creacion,
        )

        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)

        return self._to_entity(model)

    def get_all(self) -> list[Post]:
        """Return all stored posts ordered by identifier."""

        statement = select(PostModel).order_by(PostModel.id.asc())

        models = self._session.scalars(statement).all()

        return [self._to_entity(model) for model in models]

    def get_by_id(self, post_id: int) -> Post | None:
        """Return a post by its identifier."""

        statement = select(PostModel).where(PostModel.id == post_id)

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_entity(model)

    def delete(self, post_id: int) -> bool:
        """Delete a post by its identifier."""

        statement = select(PostModel).where(PostModel.id == post_id)

        model = self._session.scalar(statement)

        if model is None:
            return False

        self._session.delete(model)
        self._session.commit()

        return True

    @staticmethod
    def _to_entity(model: PostModel) -> Post:
        """Convert an ORM model into a domain entity."""

        return Post(
            id=model.id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            resumen=json.loads(model.resumen),
            fecha_creacion=model.fecha_creacion,
        )
