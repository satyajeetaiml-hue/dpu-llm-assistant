"""Ingest local documents into Azure AI Search.

Walks the ``documents/`` tree, treating each top-level folder name as the
document category, then chunks, embeds and indexes every .txt/.md file.

    python scripts/ingest_documents.py [--root documents]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.rag.indexing import index_document  # noqa: E402
from app.services.ai_search import get_search_service  # noqa: E402

SUPPORTED_SUFFIXES = {".txt", ".md"}
VALID_CATEGORIES = {"admissions", "policies", "ciqa", "examination", "syllabus"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents into Azure AI Search")
    parser.add_argument("--root", default="documents", help="Root documents directory")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Documents root not found: {root}")

    get_search_service().ensure_index()

    total_files = 0
    total_chunks = 0
    for path in root.rglob("*"):
        if path.suffix.lower() not in SUPPORTED_SUFFIXES or not path.is_file():
            continue
        # Category = first path segment under root.
        rel = path.relative_to(root)
        category = rel.parts[0] if rel.parts else "policies"
        if category not in VALID_CATEGORIES:
            print(f"Skipping '{rel}' (unknown category '{category}')")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        chunks = index_document(text=text, source=str(rel), category=category)
        total_files += 1
        total_chunks += chunks
        print(f"Indexed {chunks:4d} chunks  <-  {rel}")

    print(f"\nDone. {total_files} files, {total_chunks} chunks indexed.")


if __name__ == "__main__":
    main()
