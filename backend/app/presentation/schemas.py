# backend/app/presentation/schemas.py
"""API request and response schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SummaryResponse(BaseModel):
    """Summary information returned for a post."""

    summary: str
    keywords: list[str] = Field(default_factory=list)

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )


class PostResponse(BaseModel):
    """API response representing a post."""

    id: int
    title: str
    description: str
    summary: SummaryResponse
    file_path: str | None = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )
