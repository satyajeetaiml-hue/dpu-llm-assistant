"""Application configuration.

Settings are loaded from environment variables (see ``.env.example``) using
pydantic-settings. A single cached ``Settings`` instance is exposed via
``get_settings()`` so the same configuration is reused across the app.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- General ---------------------------------------------------------
    app_name: str = "University AI Assistant"
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    api_prefix: str = "/api"
    cors_origins: list[str] = Field(default=["http://localhost:5173"])

    # --- Azure AI Foundry / Azure OpenAI ---------------------------------
    azure_openai_endpoint: str = Field(default="", alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str = Field(default="", alias="AZURE_OPENAI_API_KEY")
    azure_openai_api_version: str = Field(
        default="2024-10-21", alias="AZURE_OPENAI_API_VERSION"
    )
    azure_openai_chat_deployment: str = Field(
        default="gpt-4o", alias="AZURE_OPENAI_CHAT_DEPLOYMENT"
    )
    azure_openai_embedding_deployment: str = Field(
        default="text-embedding-3-large", alias="AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
    )

    # --- Azure AI Search -------------------------------------------------
    azure_search_endpoint: str = Field(default="", alias="AZURE_SEARCH_ENDPOINT")
    azure_search_api_key: str = Field(default="", alias="AZURE_SEARCH_API_KEY")
    azure_search_index_name: str = Field(
        default="university-docs", alias="AZURE_SEARCH_INDEX_NAME"
    )

    # --- Azure Blob Storage ----------------------------------------------
    azure_storage_connection_string: str = Field(
        default="", alias="AZURE_STORAGE_CONNECTION_STRING"
    )
    azure_storage_container: str = Field(
        default="documents", alias="AZURE_STORAGE_CONTAINER"
    )

    # --- Auth ------------------------------------------------------------
    jwt_secret: str = Field(default="change-me", alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_expiry_minutes: int = Field(default=60, alias="JWT_EXPIRY_MINUTES")

    # --- RAG tuning ------------------------------------------------------
    chunk_size: int = 800
    chunk_overlap: int = 120
    retrieval_top_k: int = 5
    embedding_dimensions: int = 3072


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()
