# backend/app/presentation/router.py
"""API routing and endpoint definitions."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.application.ports.storage_service import StoragePort
from app.application.ports.summarizer_service import SummarizerPort
from app.application.use_cases.create_post import CreatePostUseCase
from app.application.use_cases.delete_post import DeletePostUseCase
from app.application.use_cases.list_posts import ListPostsUseCase
from app.core.logging import get_logger
from app.domain.interfaces.post_repository import PostRepository
from app.infrastructure.database import get_engine
from app.presentation.dependencies import (
    get_post_repository,
    get_storage_service,
    get_summarizer_service,
)
from app.presentation.mappers import PostMapper
from app.presentation.schemas import PostResponse

logger = get_logger(__name__)

router = APIRouter()


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
        content={"status": "ok", "database": database},
    )


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
    return PostMapper.to_response_list(posts)


@router.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Posts"],
    summary="Create post",
)
def create_post(
    title: str = Form(..., min_length=1, max_length=200, description="Post title"),
    description: str = Form(..., min_length=1, description="Post description"),
    file: UploadFile | None = File(None, description="Optional file attachment"),
    repository: PostRepository = Depends(get_post_repository),
    summarizer: SummarizerPort = Depends(get_summarizer_service),
    storage: StoragePort = Depends(get_storage_service),
) -> PostResponse:
    """Create a new post."""
    use_case = CreatePostUseCase(
        repository=repository,
        summarizer=summarizer,
        storage=storage,
    )

    post = use_case.execute(
        title=title,
        description=description,
        file_data=file.file if file else None,
        filename=file.filename if file else None,
    )

    return PostMapper.to_response(post)


@router.delete(
    "/api/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Posts"],
    summary="Delete post",
)
def delete_post(
    post_id: int,
    repository: PostRepository = Depends(get_post_repository),
    storage: StoragePort = Depends(get_storage_service),
) -> Response:
    """Delete a post and its associated file."""
    use_case = DeletePostUseCase(
        repository=repository,
        storage=storage,
    )

    use_case.execute(post_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
