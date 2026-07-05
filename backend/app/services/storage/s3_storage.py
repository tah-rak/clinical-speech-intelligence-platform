"""AWS S3 storage provider (optional)."""

import logging
import tempfile
from pathlib import Path

from app.core.config import get_settings
from app.services.storage.base import StorageProvider

logger = logging.getLogger(__name__)
settings = get_settings()


class S3StorageProvider(StorageProvider):
    def __init__(self) -> None:
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import boto3

                self._client = boto3.client(
                    "s3",
                    region_name=settings.AWS_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID or None,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY or None,
                )
            except ImportError:
                raise RuntimeError("boto3 is required for S3 storage. Install with: pip install boto3")
        return self._client

    async def save(self, file_content: bytes, filename: str, visit_id: str) -> str:
        if not settings.AWS_S3_BUCKET:
            raise RuntimeError("AWS_S3_BUCKET is not configured")

        key = f"audio/{visit_id}/{filename}"
        client = self._get_client()
        client.put_object(
            Bucket=settings.AWS_S3_BUCKET,
            Key=key,
            Body=file_content,
            ContentType="audio/mpeg",
        )
        return f"s3://{settings.AWS_S3_BUCKET}/{key}"

    async def get_path(self, storage_uri: str) -> Path | None:
        if not storage_uri.startswith("s3://"):
            return Path(storage_uri) if Path(storage_uri).exists() else None

        parts = storage_uri.replace("s3://", "").split("/", 1)
        if len(parts) != 2:
            return None

        bucket, key = parts
        client = self._get_client()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=Path(key).suffix)
        try:
            client.download_fileobj(bucket, key, tmp)
            tmp.close()
            return Path(tmp.name)
        except Exception as e:
            logger.error("Failed to download from S3: %s", e)
            return None

    def get_provider_name(self) -> str:
        return "s3"
