"""Retrieval layer: turn a user query into grounded context passages."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.config import get_settings
from app.services.ai_search import get_search_service
from app.services.embeddings import get_embedding_service


@dataclass
class RetrievedPassage:
    content: str
    source: str
    category: str
    page: int

    @classmethod
    def from_doc(cls, doc: dict[str, Any]) -> "RetrievedPassage":
        return cls(
            content=doc.get("content", ""),
            source=doc.get("source", "unknown"),
            category=doc.get("category", "unknown"),
            page=doc.get("page", 0),
        )


def retrieve(
    query: str,
    *,
    top_k: int | None = None,
    category: str | None = None,
) -> list[RetrievedPassage]:
    """Embed the query and run hybrid search against Azure AI Search."""
    top_k = top_k or get_settings().retrieval_top_k
    query_vector = get_embedding_service().embed_one(query)
    docs = get_search_service().hybrid_search(
        query_text=query,
        query_vector=query_vector,
        top_k=top_k,
        category=category,
    )
    return [RetrievedPassage.from_doc(d) for d in docs]


def format_context(passages: list[RetrievedPassage]) -> str:
    """Render passages into a numbered, citeable context block."""
    if not passages:
        return "No relevant documents were found."
    lines = []
    for i, p in enumerate(passages, start=1):
        lines.append(f"[{i}] (source: {p.source}, page: {p.page})\n{p.content}")
    return "\n\n".join(lines)
