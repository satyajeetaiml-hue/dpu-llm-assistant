"""Sync local documents to Azure Blob Storage.

Uploads every file under ``documents/`` to the configured container, preserving
the ``<category>/<filename>`` layout used by the upload API.

    python scripts/sync_blob_storage.py [--root documents]
"""
from __future__ import annotations

import argparse
import mimetypes
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.services.blob_storage import get_blob_service  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync documents to Blob Storage")
    parser.add_argument("--root", default="documents", help="Root documents directory")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Documents root not found: {root}")

    blob = get_blob_service()
    blob.ensure_container()

    count = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        url = blob.upload(blob_name=rel, data=path.read_bytes(), content_type=content_type)
        count += 1
        print(f"Uploaded {rel}  ->  {url}")

    print(f"\nDone. {count} files synced.")


if __name__ == "__main__":
    main()
