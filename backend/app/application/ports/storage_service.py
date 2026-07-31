# backend/app/application/ports/storage_service.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import BinaryIO


class StoragePort(ABC):
    """Port for file storage operations."""

    @abstractmethod
    def save_file(self, file_data: BinaryIO, path: str) -> str:
        """Persist a file and return its storage path."""

    @abstractmethod
    def delete_file(self, path: str) -> bool:
        """Delete a file from storage."""
