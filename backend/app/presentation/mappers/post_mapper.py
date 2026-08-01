# backend/app/presentation/mappers/post_mapper.py
"""Mapper for converting domain entities to API responses."""

from __future__ import annotations

from app.domain.entities.post import Post
from app.presentation.schemas import PostResponse, SummaryResponse


class PostMapper:
    """Mapper for converting domain entities to API responses."""

    @staticmethod
    def to_response(post: Post) -> PostResponse:
        """Convert a Post entity to a PostResponse DTO."""
        summary_data = post.summary

        if not isinstance(summary_data, dict):
            summary_data = {"summary": "", "keywords": []}

        return PostResponse(
            id=post.id,
            title=post.title,
            description=post.description,
            summary=SummaryResponse(**summary_data),
            file_path=post.file_path,
            created_at=post.created_at,
        )

    @staticmethod
    def to_response_list(posts: list[Post]) -> list[PostResponse]:
        """Convert a list of Post entities to a list of PostResponse DTOs."""
        return [PostMapper.to_response(post) for post in posts]
