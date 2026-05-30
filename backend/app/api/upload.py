"""Document upload endpoint: persist to blob storage and index for RAG."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.core.logging import get_logger
from app.models.response_models import UploadResponse
from app.rag.indexing import index_document
from app.services.auth import get_current_user
from app.services.blob_storage import get_blob_service

logger = get_logger(__name__)
router = APIRouter(tags=["upload"])

_VALID_CATEGORIES = {"admissions", "policies", "ciqa", "examination", "syllabus"}


def _extract_text(filename: str, data: bytes) -> str:
    """Best-effort text extraction.

    Plain-text/markdown is decoded directly. PDF/Docx parsing is left as a
    TODO hook so the dependency set stays light for the scaffold.
    """
    lower = filename.lower()
    if lower.endswith((".txt", ".md")):
        return data.decode("utf-8", errors="ignore")
    # TODO: plug in PDF/DOCX extraction (e.g. pypdf, python-docx).
    raise HTTPException(
        status_code=415,
        detail=f"Unsupported file type for '{filename}'. Only .txt/.md are parsed in this scaffold.",
    )


@router.post("/upload", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(...),
    category: str = Form(...),
    user: dict[str, Any] = Depends(get_current_user),
) -> UploadResponse:
    if category not in _VALID_CATEGORIES:
        raise HTTPException(status_code=422, detail=f"Invalid category '{category}'")

    data = await file.read()
    filename = file.filename or "uploaded"

    blob = get_blob_service()
    blob.ensure_container()
    blob_url = blob.upload(
        blob_name=f"{category}/{filename}",
        data=data,
        content_type=file.content_type or "application/octet-stream",
    )

    text = _extract_text(filename, data)
    chunks = index_document(text=text, source=filename, category=category)

    return UploadResponse(
        filename=filename,
        blob_url=blob_url,
        chunks_indexed=chunks,
        category=category,
    )
