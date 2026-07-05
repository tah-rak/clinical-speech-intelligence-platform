"""Storage provider interface."""

from abc import ABC, abstractmethod
from pathlib import Path


class StorageProvider(ABC):
    @abstractmethod
    async def save(self, file_content: bytes, filename: str, visit_id: str) -> str:
        """Save file and return storage URI."""

    @abstractmethod
    async def get_path(self, storage_uri: str) -> Path | None:
        """Get local path for processing."""

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider identifier."""
