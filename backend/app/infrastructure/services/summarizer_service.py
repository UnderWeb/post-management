# backend/app/infrastructure/services/summarizer_service.py
from __future__ import annotations

import re
from collections import Counter
from typing import Any

from app.application.ports.summarizer_service import SummarizerPort

_SPANISH_STOPWORDS: set[str] = {
    "de",
    "la",
    "que",
    "el",
    "en",
    "y",
    "a",
    "los",
    "del",
    "se",
    "las",
    "por",
    "un",
    "para",
    "con",
    "no",
    "una",
    "su",
    "al",
    "lo",
    "como",
    "más",
    "pero",
    "sus",
    "le",
    "ya",
    "o",
    "este",
    "sí",
    "porque",
    "esta",
    "entre",
    "cuando",
    "muy",
    "sin",
    "sobre",
    "también",
    "me",
    "hasta",
    "hay",
    "donde",
    "quien",
    "desde",
}

_ENGLISH_STOPWORDS: set[str] = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "have",
    "will",
    "would",
    "there",
    "their",
    "about",
    "into",
    "your",
    "after",
    "before",
    "could",
    "should",
    "being",
    "been",
    "were",
    "they",
    "them",
    "then",
    "than",
    "what",
    "when",
    "where",
}

_STOPWORDS = _SPANISH_STOPWORDS | _ENGLISH_STOPWORDS

_SUMMARY_MAX_LENGTH = 150
_KEYWORDS_COUNT = 5


class LexicalSummarizerService(SummarizerPort):
    """
    Deterministic lexical summarizer.

    Generates the first sentence as summary and extracts
    the five most frequent significant words.
    """

    def summarize(self, text: str) -> dict[str, Any]:
        if not text.strip():
            return {
                "summary": "",
                "keywords": [],
            }

        summary = text.strip().split(".")[0].strip()

        if len(summary) > _SUMMARY_MAX_LENGTH:
            summary = summary[:_SUMMARY_MAX_LENGTH].rstrip()

        words = re.findall(
            r"\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]{3,}\b",
            text.lower(),
        )

        words = [word for word in words if word not in _STOPWORDS]

        counter = Counter(words)

        keywords = [word for word, _ in counter.most_common(_KEYWORDS_COUNT)]

        return {
            "summary": summary,
            "keywords": keywords,
        }
