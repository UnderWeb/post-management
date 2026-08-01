# backend/app/application/ports/__init__.py
"""Application ports module."""

from app.application.ports.storage_service import StoragePort
from app.application.ports.summarizer_service import (
    SummarizerPort,
    SummaryResult,
)

__all__ = [
    "StoragePort",
    "SummarizerPort",
    "SummaryResult",
]
