# backend/app/domain/entities/post.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class Post:
    """Domain entity representing a post."""

    title: str
    description: str
    id: int | None = None
    summary: dict[str, Any] = field(default_factory=dict)
    file_path: str | None = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
