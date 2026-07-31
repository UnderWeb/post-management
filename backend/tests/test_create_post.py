# backend/tests/test_create_post.py
from __future__ import annotations

import pytest

from app.application.use_cases.create_post import CreatePostUseCase
from app.domain.entities.post import Post
from tests.conftest import (
    MockPostRepository,
    MockSummarizer,
)


class TestCreatePostUseCase:
    """Tests for the CreatePostUseCase."""

    def test_successful_creation(
        self,
        empty_repository: MockPostRepository,
        mock_summarizer: MockSummarizer,
    ) -> None:
        """Valid input should create and return a Post entity."""

        use_case = CreatePostUseCase(
            repository=empty_repository,
            summarizer=mock_summarizer,
        )

        result = use_case.execute(
            nombre="Test Post",
            descripcion="A test description.",
        )

        assert isinstance(result, Post)
        assert result.id > 0
        assert result.nombre == "Test Post"
        assert result.descripcion == "A test description."

        assert result.resumen == {
            "summary": "Auto-generated summary from text.",
            "keywords": [
                "auto",
                "generated",
                "summary",
            ],
        }

        assert result.fecha_creacion is not None

    def test_empty_nombre_raises_error(
        self,
        empty_repository: MockPostRepository,
        mock_summarizer: MockSummarizer,
    ) -> None:
        """Empty nombre should raise ValueError."""

        use_case = CreatePostUseCase(
            repository=empty_repository,
            summarizer=mock_summarizer,
        )

        with pytest.raises(ValueError, match="nombre"):
            use_case.execute(
                nombre="",
                descripcion="Some description",
            )

    def test_empty_descripcion_raises_error(
        self,
        empty_repository: MockPostRepository,
        mock_summarizer: MockSummarizer,
    ) -> None:
        """Empty descripcion should raise ValueError."""

        use_case = CreatePostUseCase(
            repository=empty_repository,
            summarizer=mock_summarizer,
        )

        with pytest.raises(ValueError, match="descripcion"):
            use_case.execute(
                nombre="Title",
                descripcion="",
            )

    def test_whitespace_only_nombre_raises_error(
        self,
        empty_repository: MockPostRepository,
        mock_summarizer: MockSummarizer,
    ) -> None:
        """Whitespace-only nombre should raise ValueError."""

        use_case = CreatePostUseCase(
            repository=empty_repository,
            summarizer=mock_summarizer,
        )

        with pytest.raises(ValueError, match="nombre"):
            use_case.execute(
                nombre="   ",
                descripcion="Valid description",
            )
