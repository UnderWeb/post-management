# backend/app/infrastructure/services/__init__.py
from app.infrastructure.services.summarizer_service import (
    LexicalSummarizerService,
)

__all__ = [
    "LexicalSummarizerService",
]
