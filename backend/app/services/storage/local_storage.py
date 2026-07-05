"""Local filesystem storage provider."""

import os
from pathlib import Path

from app.core.config import get_settings
from app.services.storage.base import StorageProvider

settings = get_settings()


class LocalStorageProvider(StorageProvider):
    def __init__(self) -> None:
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, file_content: bytes, filename: str, visit_id: str) -> str:
        visit_dir = self.upload_dir / visit_id
        visit_dir.mkdir(parents=True, exist_ok=True)
        safe_name = os.path.basename(filename)
        file_path = visit_dir / safe_name
        file_path.write_bytes(file_content)
        return str(file_path)

    async def get_path(self, storage_uri: str) -> Path | None:
        path = Path(storage_uri)
        return path if path.exists() else None

    def get_provider_name(self) -> str:
        return "local"
