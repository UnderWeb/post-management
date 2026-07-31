# backend/app/application/ports/summarizer_service.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypedDict


class SummaryResult(TypedDict):
    """Result returned by the summarizer service."""

    summary: str
    keywords: list[str]


class SummarizerPort(ABC):
    """Port for text summarization."""

    @abstractmethod
    def summarize(self, text: str) -> SummaryResult:
        """Generate a summary and keywords from text."""
