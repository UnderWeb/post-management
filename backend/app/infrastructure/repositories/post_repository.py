# backend/app/infrastructure/repositories/post_repository.py
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.post import Post
from app.domain.interfaces.post_repository import PostRepository
from app.infrastructure.database.models.post_model import PostModel


class SqlAlchemyPostRepository(PostRepository):
    """SQLAlchemy implementation of PostRepository."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, post: Post) -> Post:
        model = PostModel(
            nombre=post.nombre,
            descripcion=post.descripcion,
            resumen=post.resumen,
            fecha_creacion=post.fecha_creacion,
        )

        self.session.add(model)
        self.session.flush()

        return self._to_entity(model)

    def get_all(self) -> list[Post]:
        result = self.session.execute(
            select(PostModel)
        )

        return [
            self._to_entity(item)
            for item in result.scalars().all()
        ]

    def get_by_id(self, post_id: int) -> Post | None:
        model = self.session.get(
            PostModel,
            post_id,
        )

        if model is None:
            return None

        return self._to_entity(model)

    def delete(self, post_id: int) -> bool:
        model = self.session.get(
            PostModel,
            post_id,
        )

        if model is None:
            return False

        self.session.delete(model)

        return True

    @staticmethod
    def _to_entity(model: PostModel) -> Post:
        return Post(
            id=model.id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            resumen=model.resumen,
            fecha_creacion=model.fecha_creacion,
        )
