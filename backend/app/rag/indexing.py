"""Document indexing pipeline: chunk -> embed -> push to Azure AI Search."""
from __future__ import annotations

import hashlib
from typing import Any

from app.core.logging import get_logger
from app.rag.chunking import chunk_text
from app.services.ai_search import get_search_service
from app.services.embeddings import get_embedding_service

logger = get_logger(__name__)


def _doc_id(source: str, chunk_index: int) -> str:
    digest = hashlib.sha1(f"{source}:{chunk_index}".encode()).hexdigest()
    return digest


def index_document(
    *,
    text: str,
    source: str,
    category: str,
    page: int = 0,
) -> int:
    """Chunk, embed and upload a single document. Returns chunk count."""
    chunks = chunk_text(text)
    if not chunks:
        logger.warning("No chunks produced for source '%s'", source)
        return 0

    embeddings = get_embedding_service().embed([c.content for c in chunks])
    documents: list[dict[str, Any]] = []
    for chunk, vector in zip(chunks, embeddings):
        documents.append(
            {
                "id": _doc_id(source, chunk.index),
                "content": chunk.content,
                "source": source,
                "category": category,
                "page": page,
                "content_vector": vector,
            }
        )

    get_search_service().upload_documents(documents)
    logger.info("Indexed %d chunks from '%s'", len(documents), source)
    return len(documents)
