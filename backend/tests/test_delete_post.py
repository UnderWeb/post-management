# backend/tests/test_delete_post.py
"""Tests for the DeletePostUseCase."""

from __future__ import annotations

import pytest

from app.application.use_cases.delete_post import DeletePostUseCase
from app.core.exceptions import NotFoundError
from tests.conftest import (
    SAMPLE_POST_1,
    MockPostRepository,
    MockStorageService,
)


class TestDeletePostUseCase:
    """Tests for the DeletePostUseCase."""

    def test_successful_delete(
        self,
        mock_repository: MockPostRepository,
        mock_storage: MockStorageService,
    ) -> None:
        """Deleting an existing post should return True."""
        use_case = DeletePostUseCase(
            repository=mock_repository,
            storage=mock_storage,
        )

        result = use_case.execute(post_id=SAMPLE_POST_1.id)

        assert result is True
        assert mock_repository.get_by_id(SAMPLE_POST_1.id) is None

    def test_delete_nonexistent_raises_error(
        self,
        mock_repository: MockPostRepository,
        mock_storage: MockStorageService,
    ) -> None:
        """Deleting a missing post should raise NotFoundError."""
        use_case = DeletePostUseCase(
            repository=mock_repository,
            storage=mock_storage,
        )

        with pytest.raises(NotFoundError):
            use_case.execute(post_id=9999)
