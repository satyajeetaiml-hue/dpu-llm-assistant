"""Azure AI Foundry / Azure OpenAI chat client.

Wraps the Azure OpenAI chat-completions endpoint behind a small async-friendly
interface used by the agents. The client is created lazily and cached.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

from openai import AzureOpenAI

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

ChatMessage = dict[str, str]


@lru_cache
def _client() -> AzureOpenAI:
    settings = get_settings()
    return AzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
    )


class AzureFoundryClient:
    """Thin wrapper over Azure OpenAI chat completions."""

    def __init__(self) -> None:
        self._settings = get_settings()

    def chat(
        self,
        messages: list[ChatMessage],
        *,
        temperature: float = 0.2,
        max_tokens: int = 1024,
        tools: list[dict[str, Any]] | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> Any:
        """Run a chat completion and return the raw response object."""
        kwargs: dict[str, Any] = {
            "model": self._settings.azure_openai_chat_deployment,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            kwargs["tools"] = tools
        if response_format:
            kwargs["response_format"] = response_format

        logger.debug("Azure chat completion with %d messages", len(messages))
        return _client().chat.completions.create(**kwargs)

    def complete_text(self, messages: list[ChatMessage], **kwargs: Any) -> str:
        """Convenience helper that returns just the assistant text."""
        response = self.chat(messages, **kwargs)
        return response.choices[0].message.content or ""


@lru_cache
def get_foundry_client() -> AzureFoundryClient:
    return AzureFoundryClient()
