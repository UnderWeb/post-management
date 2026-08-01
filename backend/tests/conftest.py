# backend/tests/conftest.py
"""Shared test fixtures and mocks."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, BinaryIO

import pytest
from fastapi.testclient import TestClient

from app.application.ports.storage_service import StoragePort
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
    title="First Post",
    description="Description of the first post.",
    summary=SAMPLE_SUMMARY,
    created_at=datetime(
        2025,
        1,
        15,
        10,
        0,
        0,
        tzinfo=UTC,
    ),
)


SAMPLE_POST_2 = Post(
    id=2,
    title="Second Post",
    description="Description of the second post.",
    summary={
        "summary": "Another sample summary.",
        "keywords": [
            "another",
            "sample",
        ],
    },
    created_at=datetime(
        2025,
        1,
        16,
        12,
        0,
        0,
        tzinfo=UTC,
    ),
)


class MockPostRepository(PostRepository):
    """In-memory repository used for tests."""

    def __init__(self) -> None:
        self._store: dict[int, Post] = {}
        self._next_id = 1

    def seed(self, posts: list[Post]) -> None:
        for post in posts:
            self._store[post.id] = post
            self._next_id = max(self._next_id, post.id + 1)

    def create(self, post: Post) -> Post:
        created = Post(
            id=self._next_id,
            title=post.title,
            description=post.description,
            summary=post.summary,
            file_path=post.file_path,
            created_at=post.created_at,
        )

        self._store[self._next_id] = created
        self._next_id += 1

        return created

    def list(self) -> list[Post]:
        return list(self._store.values())

    def get_by_id(self, post_id: int) -> Post | None:
        return self._store.get(post_id)

    def delete(self, post_id: int) -> bool:
        if post_id not in self._store:
            return False

        del self._store[post_id]
        return True


class MockSummarizer(SummarizerPort):
    """Deterministic summarizer mock."""

    def summarize(self, text: str) -> dict[str, Any]:
        return {
            "summary": "Auto-generated summary from text.",
            "keywords": [
                "auto",
                "generated",
                "summary",
            ],
        }


class MockStorageService(StoragePort):
    """In-memory storage mock for tests."""

    def __init__(self) -> None:
        self._files: dict[str, bytes] = {}

    def save_file(self, file_data: BinaryIO, path: str) -> str:
        stored_path = f"/mock/uploads/{path}"
        self._files[stored_path] = file_data.read()
        return stored_path

    def delete_file(self, path: str) -> bool:
        if path in self._files:
            del self._files[path]
            return True
        return False


@pytest.fixture
def mock_repository() -> MockPostRepository:
    repository = MockPostRepository()
    repository.seed([SAMPLE_POST_1, SAMPLE_POST_2])
    return repository


@pytest.fixture
def empty_repository() -> MockPostRepository:
    return MockPostRepository()


@pytest.fixture
def mock_summarizer() -> MockSummarizer:
    return MockSummarizer()


@pytest.fixture
def mock_storage() -> MockStorageService:
    return MockStorageService()


@pytest.fixture
def client(
    mock_repository: MockPostRepository,
    mock_summarizer: MockSummarizer,
    mock_storage: MockStorageService,
) -> TestClient:
    app.dependency_overrides[dependencies.get_post_repository] = lambda: mock_repository
    app.dependency_overrides[dependencies.get_summarizer_service] = (
        lambda: mock_summarizer
    )
    app.dependency_overrides[dependencies.get_storage_service] = lambda: mock_storage

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
