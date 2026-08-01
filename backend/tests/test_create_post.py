# backend/tests/test_create_post.py
"""Tests for the CreatePostUseCase."""

from __future__ import annotations

import pytest

from app.application.use_cases.create_post import CreatePostUseCase
from app.domain.entities.post import Post
from tests.conftest import (
    MockPostRepository,
    MockStorageService,
    MockSummarizer,
)


class TestCreatePostUseCase:
    """Tests for the CreatePostUseCase."""

    def test_successful_creation(
        self,
        empty_repository: MockPostRepository,
        mock_summarizer: MockSummarizer,
        mock_storage: MockStorageService,
    ) -> None:
        """Valid input should create and return a Post entity."""
        use_case = CreatePostUseCase(
            repository=empty_repository,
            summarizer=mock_summarizer,
            storage=mock_storage,
        )

        result = use_case.execute(
            title="Test Post",
            description="A test description.",
        )

        assert isinstance(result, Post)
        assert result.id > 0
        assert result.title == "Test Post"
        assert result.description == "A test description."
        assert result.summary == {
            "summary": "Auto-generated summary from text.",
            "keywords": ["auto", "generated", "summary"],
        }
        assert result.created_at is not None

    def test_empty_title_raises_error(
        self,
        empty_repository: MockPostRepository,
        mock_summarizer: MockSummarizer,
        mock_storage: MockStorageService,
    ) -> None:
        """Empty title should raise ValueError."""
        use_case = CreatePostUseCase(
            repository=empty_repository,
            summarizer=mock_summarizer,
            storage=mock_storage,
        )

        with pytest.raises(ValueError, match="title"):
            use_case.execute(
                title="",
                description="Some description",
            )

    def test_empty_description_raises_error(
        self,
        empty_repository: MockPostRepository,
        mock_summarizer: MockSummarizer,
        mock_storage: MockStorageService,
    ) -> None:
        """Empty description should raise ValueError."""
        use_case = CreatePostUseCase(
            repository=empty_repository,
            summarizer=mock_summarizer,
            storage=mock_storage,
        )

        with pytest.raises(ValueError, match="description"):
            use_case.execute(
                title="Title",
                description="",
            )

    def test_whitespace_only_title_raises_error(
        self,
        empty_repository: MockPostRepository,
        mock_summarizer: MockSummarizer,
        mock_storage: MockStorageService,
    ) -> None:
        """Whitespace-only title should raise ValueError."""
        use_case = CreatePostUseCase(
            repository=empty_repository,
            summarizer=mock_summarizer,
            storage=mock_storage,
        )

        with pytest.raises(ValueError, match="title"):
            use_case.execute(
                title="   ",
                description="Valid description",
            )
