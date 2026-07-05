"""Storage provider factory."""

from app.core.config import get_settings
from app.services.storage.base import StorageProvider
from app.services.storage.local_storage import LocalStorageProvider
from app.services.storage.s3_storage import S3StorageProvider

settings = get_settings()


def get_storage_provider() -> StorageProvider:
    if settings.effective_storage_provider == "s3":
        try:
            return S3StorageProvider()
        except Exception:
            return LocalStorageProvider()
    return LocalStorageProvider()
