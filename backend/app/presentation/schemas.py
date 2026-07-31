# backend/app/presentation/schemas.py
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


class PostCreateRequest(BaseModel):
    """Request payload used to create a post."""

    nombre: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Post title",
    )

    descripcion: str = Field(
        ...,
        min_length=1,
        description="Post description",
    )

    model_config = ConfigDict(
        extra="forbid",
    )


class PostResponse(BaseModel):
    """API response representing a post."""

    id: int
    nombre: str
    descripcion: str
    resumen: SummaryResponse
    fecha_creacion: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )
