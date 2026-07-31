# backend/tests/test_list_posts.py
from __future__ import annotations

from app.application.use_cases.list_posts import ListPostsUseCase
from tests.conftest import (
    MockPostRepository,
    SAMPLE_POST_1,
    SAMPLE_POST_2,
)


class TestListPostsUseCase:

    def test_returns_list_of_posts(
        self,
        mock_repository: MockPostRepository,
    ) -> None:

        use_case = ListPostsUseCase(
            repository=mock_repository,
        )

        result = use_case.execute()

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].id == SAMPLE_POST_1.id
        assert result[1].id == SAMPLE_POST_2.id


    def test_empty_list(
        self,
        empty_repository: MockPostRepository,
    ) -> None:

        use_case = ListPostsUseCase(
            repository=empty_repository,
        )

        result = use_case.execute()

        assert result == []
