# backend/tests/test_post_repository_contract.py
"""Tests for PostRepository expected behavior."""

from __future__ import annotations

from tests.conftest import (
    SAMPLE_POST_1,
    MockPostRepository,
)


class TestPostRepositoryContract:
    """Tests for PostRepository expected behavior."""

    def test_get_by_id_existing_post(self, mock_repository: MockPostRepository) -> None:
        """Existing post should be returned by id."""
        result = mock_repository.get_by_id(SAMPLE_POST_1.id)

        assert result is not None
        assert result.id == SAMPLE_POST_1.id
        assert result.title == SAMPLE_POST_1.title

    def test_get_by_id_missing_post(self, empty_repository: MockPostRepository) -> None:
        """Missing post should return None."""
        result = empty_repository.get_by_id(9999)
        assert result is None
