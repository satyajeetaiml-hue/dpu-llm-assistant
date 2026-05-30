"""Azure Blob Storage service for raw document persistence."""
from __future__ import annotations

from functools import lru_cache

from azure.storage.blob import BlobServiceClient, ContentSettings

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@lru_cache
def _service_client() -> BlobServiceClient:
    s = get_settings()
    return BlobServiceClient.from_connection_string(s.azure_storage_connection_string)


class BlobStorageService:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._container = self._settings.azure_storage_container

    def ensure_container(self) -> None:
        client = _service_client().get_container_client(self._container)
        if not client.exists():
            client.create_container()
            logger.info("Created blob container '%s'", self._container)

    def upload(
        self,
        blob_name: str,
        data: bytes,
        *,
        content_type: str = "application/octet-stream",
    ) -> str:
        """Upload bytes and return the blob URL."""
        blob = _service_client().get_blob_client(
            container=self._container, blob=blob_name
        )
        blob.upload_blob(
            data,
            overwrite=True,
            content_settings=ContentSettings(content_type=content_type),
        )
        logger.info("Uploaded blob '%s' (%d bytes)", blob_name, len(data))
        return blob.url

    def download(self, blob_name: str) -> bytes:
        blob = _service_client().get_blob_client(
            container=self._container, blob=blob_name
        )
        return blob.download_blob().readall()

    def list_blobs(self, prefix: str | None = None) -> list[str]:
        client = _service_client().get_container_client(self._container)
        return [b.name for b in client.list_blobs(name_starts_with=prefix)]


@lru_cache
def get_blob_service() -> BlobStorageService:
    return BlobStorageService()
