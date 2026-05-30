"""Embedding generation via Azure OpenAI."""
from __future__ import annotations

from functools import lru_cache

from openai import AzureOpenAI

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@lru_cache
def _client() -> AzureOpenAI:
    settings = get_settings()
    return AzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
    )


class EmbeddingService:
    def __init__(self) -> None:
        self._settings = get_settings()

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding vector per input text."""
        if not texts:
            return []
        logger.debug("Embedding %d text(s)", len(texts))
        response = _client().embeddings.create(
            model=self._settings.azure_openai_embedding_deployment,
            input=texts,
        )
        return [item.embedding for item in response.data]

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()
