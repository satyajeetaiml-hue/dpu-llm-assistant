"""Text chunking utilities for document ingestion.

Splits long documents into overlapping, word-bounded chunks suitable for
embedding and indexing.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from app.core.config import get_settings

_WHITESPACE = re.compile(r"\s+")


@dataclass
class Chunk:
    content: str
    index: int


def normalize(text: str) -> str:
    """Collapse runs of whitespace into single spaces."""
    return _WHITESPACE.sub(" ", text).strip()


def chunk_text(
    text: str,
    *,
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """Split text into overlapping chunks of roughly ``chunk_size`` words.

    Overlap is expressed in words and copied from the tail of the previous
    chunk to preserve context across boundaries.
    """
    settings = get_settings()
    chunk_size = chunk_size or settings.chunk_size
    overlap = overlap if overlap is not None else settings.chunk_overlap

    words = normalize(text).split(" ")
    if not words or words == [""]:
        return []

    chunks: list[Chunk] = []
    step = max(chunk_size - overlap, 1)
    for idx, start in enumerate(range(0, len(words), step)):
        window = words[start : start + chunk_size]
        if not window:
            break
        chunks.append(Chunk(content=" ".join(window), index=idx))
        if start + chunk_size >= len(words):
            break
    return chunks
