# backend/tests/conftest.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.application.ports.summarizer_service import SummarizerPort
from app.domain.entities.post import Post
from app.domain.interfaces.post_repository import PostRepository
from app.main import app
from app.presentation import dependencies


SAMPLE_SUMMARY: dict[str, Any] = {
    "summary": "This is a sample summary.",
    "keywords": [
        "sample",
        "summary",
        "test",
    ],
}


SAMPLE_POST_1 = Post(
    id=1,
    nombre="First Post",
    descripcion="Description of the first post.",
    resumen=SAMPLE_SUMMARY,
        fecha_creacion=datetime(
        2025,
        1,
        15,
        10,
        0,
        0,
        tzinfo=timezone.utc,
    ),
)


SAMPLE_POST_2 = Post(
    id=2,
    nombre="Second Post",
    descripcion="Description of the second post.",
    resumen={
        "summary": "Another sample summary.",
        "keywords": [
            "another",
            "sample",
        ],
    },
    fecha_creacion=datetime(
        2025,
        1,
        16,
        12,
        0,
        0,
        tzinfo=timezone.utc,
    ),
)


class MockPostRepository(PostRepository):
    """
    In-memory repository used for tests.
    Matches the current domain contract.
    """

    def __init__(self) -> None:
        self._store: dict[int, Post] = {}
        self._next_id = 1

    def seed(
        self,
        posts: list[Post],
    ) -> None:
        for post in posts:
            self._store[post.id] = post
            self._next_id = max(
                self._next_id,
                post.id + 1,
            )

    def create(
        self,
        post: Post,
    ) -> Post:
        created = Post(
            id=self._next_id,
            nombre=post.nombre,
            descripcion=post.descripcion,
            resumen=post.resumen,
            fecha_creacion=post.fecha_creacion,
        )

        self._store[self._next_id] = created
        self._next_id += 1

        return created

    def list(self) -> list[Post]:
        return list(self._store.values())

    def get_by_id(
        self,
        post_id: int,
    ) -> Post | None:
        return self._store.get(post_id)

    def delete(
        self,
        post_id: int,
    ) -> bool:
        if post_id not in self._store:
            return False

        del self._store[post_id]

        return True


class MockSummarizer(SummarizerPort):
    """Deterministic summarizer mock."""

    def summarize(
        self,
        text: str,
    ) -> dict[str, Any]:
        return {
            "summary": "Auto-generated summary from text.",
            "keywords": [
                "auto",
                "generated",
                "summary",
            ],
        }


@pytest.fixture
def mock_repository() -> MockPostRepository:
    repository = MockPostRepository()

    repository.seed(
        [
            SAMPLE_POST_1,
            SAMPLE_POST_2,
        ]
    )

    return repository


@pytest.fixture
def empty_repository() -> MockPostRepository:
    return MockPostRepository()


@pytest.fixture
def mock_summarizer() -> MockSummarizer:
    return MockSummarizer()


@pytest.fixture
def client(
    mock_repository: MockPostRepository,
    mock_summarizer: MockSummarizer,
) -> TestClient:

    app.dependency_overrides[
        dependencies.get_post_repository
    ] = lambda: mock_repository

    app.dependency_overrides[
        dependencies.get_summarizer_service
    ] = lambda: mock_summarizer

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
