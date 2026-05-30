"""Create (or update) the Azure AI Search index.

Run once before ingesting documents:

    python scripts/build_index.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow running from repo root by adding backend/ to the path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.services.ai_search import get_search_service  # noqa: E402


def main() -> None:
    service = get_search_service()
    service.ensure_index()
    print("Search index is ready.")


if __name__ == "__main__":
    main()
