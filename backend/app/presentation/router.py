# backend/app/presentation/router.py
from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.application.use_cases.create_post import CreatePostUseCase
from app.application.use_cases.delete_post import DeletePostUseCase
from app.application.use_cases.list_posts import ListPostsUseCase
from app.core.logging import get_logger
from app.domain.entities import Post
from app.domain.interfaces.post_repository import PostRepository
from app.infrastructure.database import get_engine
from app.presentation.dependencies import (
    get_post_repository,
    get_summarizer_service,
)
from app.presentation.schemas import (
    PostCreateRequest,
    PostResponse,
)

logger = get_logger(__name__)

router = APIRouter()


# ============================================================================
# Health
# ============================================================================


@router.get(
    "/health",
    tags=["Health"],
    summary="Health check",
)
def health_check() -> JSONResponse:
    """Verify API and database availability."""

    database = "disconnected"

    try:
        with get_engine().begin() as connection:
            connection.execute(text("SELECT 1"))

        database = "connected"

    except Exception as exc:
        logger.warning("Database health check failed: %s", exc)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "ok",
            "database": database,
        },
    )


# ============================================================================
# Posts
# ============================================================================


@router.get(
    "/api/posts",
    response_model=list[PostResponse],
    tags=["Posts"],
    summary="List posts",
)
def list_posts(
    repository: PostRepository = Depends(get_post_repository),
) -> list[PostResponse]:
    """Return every stored post."""

    use_case = ListPostsUseCase(repository)

    posts = use_case.execute()

    return [_entity_to_response(post) for post in posts]


@router.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Posts"],
    summary="Create post",
)
def create_post(
    payload: PostCreateRequest,
    repository: PostRepository = Depends(get_post_repository),
    summarizer=Depends(get_summarizer_service),
) -> PostResponse:
    """Create a new post."""

    use_case = CreatePostUseCase(
        repository=repository,
        summarizer=summarizer,
    )

    post = use_case.execute(
        nombre=payload.nombre,
        descripcion=payload.descripcion,
    )

    return _entity_to_response(post)


@router.delete(
    "/api/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Posts"],
    summary="Delete post",
)
def delete_post(
    post_id: int,
    repository: PostRepository = Depends(get_post_repository),
) -> Response:
    """Delete a post."""

    use_case = DeletePostUseCase(repository)

    use_case.execute(post_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ============================================================================
# Helpers
# ============================================================================


def _entity_to_response(post: Post) -> PostResponse:
    """Convert a domain entity into an API response."""

    return PostResponse(
        id=post.id,
        nombre=post.nombre,
        descripcion=post.descripcion,
        resumen=post.resumen,
        fecha_creacion=post.fecha_creacion,
    )
