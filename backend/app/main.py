# backend/app/main.py

from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.presentation import router


setup_logging()

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Application factory."""

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="REST API for managing posts with automatic summarization.",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(router)

    register_exception_handlers(app)

    @app.middleware("http")
    async def logging_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = uuid.uuid4().hex[:8]

        start = time.perf_counter()

        logger.info(
            "request_id=%s method=%s path=%s started",
            request_id,
            request.method,
            request.url.path,
        )

        response = await call_next(request)

        elapsed = (time.perf_counter() - start) * 1000

        logger.info(
            "request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            elapsed,
        )

        response.headers["X-Request-ID"] = request_id

        return response

    logger.info(
        "%s %s started",
        settings.app_name,
        settings.app_version,
    )

    return app


app = create_app()
