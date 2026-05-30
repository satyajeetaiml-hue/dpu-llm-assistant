"""Pydantic response models for the API layer."""
from __future__ import annotations

from pydantic import BaseModel


class Citation(BaseModel):
    index: int
    source: str
    category: str
    page: int


class ChatResponse(BaseModel):
    answer: str
    agent: str
    citations: list[Citation] = []
    session_id: str | None = None


class UploadResponse(BaseModel):
    filename: str
    blob_url: str
    chunks_indexed: int
    category: str


class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str


class AdmissionMetric(BaseModel):
    program: str
    applications: int
    admitted: int
    conversion_rate: float


class AnalyticsResponse(BaseModel):
    total_applications: int
    total_admitted: int
    metrics: list[AdmissionMetric]
