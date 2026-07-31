# backend/app/domain/entities/post.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Post:
    """Domain entity representing a post."""

    nombre: str
    descripcion: str
    id: int | None = None
    resumen: dict[str, Any] = field(default_factory=dict)
    fecha_creacion: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
