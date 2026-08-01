# backend/tests/test_api_endpoints.py
"""API endpoint integration tests with mocked dependencies."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.presentation import dependencies
from tests.conftest import (
    SAMPLE_POST_1,
    SAMPLE_POST_2,
    MockPostRepository,
    MockStorageService,
    MockSummarizer,
)


class TestAPIEndpoints:
    """API endpoint tests with mocked application dependencies."""

    def setup_method(self) -> None:
        app.dependency_overrides.clear()

    def teardown_method(self) -> None:
        app.dependency_overrides.clear()

    # ------------------------------------------------------------------
    # GET /health
    # ------------------------------------------------------------------

    def test_health_check(self) -> None:
        """Health endpoint should return API status successfully."""
        with TestClient(app) as client:
            response = client.get("/health")

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"

    # ------------------------------------------------------------------
    # GET /api/posts
    # ------------------------------------------------------------------

    def test_list_posts(self) -> None:
        """GET /api/posts should return all posts."""
        repository = MockPostRepository()
        repository.seed([SAMPLE_POST_1, SAMPLE_POST_2])

        app.dependency_overrides[dependencies.get_post_repository] = lambda: repository

        with TestClient(app) as client:
            response = client.get("/api/posts")

        assert response.status_code == 200
        body = response.json()

        assert isinstance(body, list)
        assert len(body) == 2
        assert body[0]["id"] == SAMPLE_POST_1.id
        assert body[1]["id"] == SAMPLE_POST_2.id

    # ------------------------------------------------------------------
    # POST /api/posts
    # ------------------------------------------------------------------

    def test_create_post(self) -> None:
        """POST /api/posts should create a post."""
        repository = MockPostRepository()
        summarizer = MockSummarizer()
        storage = MockStorageService()

        app.dependency_overrides[dependencies.get_post_repository] = lambda: repository
        app.dependency_overrides[dependencies.get_summarizer_service] = (
            lambda: summarizer
        )
        app.dependency_overrides[dependencies.get_storage_service] = lambda: storage

        with TestClient(app) as client:
            response = client.post(
                "/api/posts",
                data={
                    "title": "New Post",
                    "description": "New description content.",
                },
            )

        assert response.status_code == 201
        body = response.json()

        assert body["id"] > 0
        assert body["title"] == "New Post"
        assert body["description"] == "New description content."
        assert "summary" in body
        assert "summary" in body["summary"]
        assert "keywords" in body["summary"]

    def test_create_post_empty_title_returns_422(self, client: TestClient) -> None:
        """Empty title should fail validation."""
        response = client.post(
            "/api/posts",
            data={
                "title": "",
                "description": "Valid description",
            },
        )
        assert response.status_code == 422

    def test_create_post_empty_description_returns_422(
        self, client: TestClient
    ) -> None:
        """Empty description should fail validation."""
        response = client.post(
            "/api/posts",
            data={
                "title": "Valid title",
                "description": "",
            },
        )
        assert response.status_code == 422

    # ------------------------------------------------------------------
    # DELETE /api/posts/{post_id}
    # ------------------------------------------------------------------

    def test_delete_post(self) -> None:
        """DELETE existing post should return 204."""
        repository = MockPostRepository()
        repository.seed([SAMPLE_POST_1])

        app.dependency_overrides[dependencies.get_post_repository] = lambda: repository
        app.dependency_overrides[dependencies.get_storage_service] = (
            lambda: MockStorageService()
        )

        with TestClient(app) as client:
            response = client.delete(f"/api/posts/{SAMPLE_POST_1.id}")

        assert response.status_code == 204
        assert repository.get_by_id(SAMPLE_POST_1.id) is None

    def test_delete_post_not_found(self) -> None:
        """DELETE missing post should return 404."""
        repository = MockPostRepository()

        app.dependency_overrides[dependencies.get_post_repository] = lambda: repository
        app.dependency_overrides[dependencies.get_storage_service] = (
            lambda: MockStorageService()
        )

        with TestClient(app) as client:
            response = client.delete("/api/posts/9999")

        assert response.status_code == 404
        body = response.json()
        assert "detail" in body
