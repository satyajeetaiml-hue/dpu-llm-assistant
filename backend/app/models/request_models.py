"""Pydantic request models for the API layer."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Role = Literal["user", "assistant", "system"]


class ChatMessage(BaseModel):
    role: Role
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User's question")
    history: list[ChatMessage] = Field(default_factory=list)
    session_id: str | None = None
    # Optional override to force routing to a specific agent.
    agent: Literal["student", "admission", "compliance", "marketing"] | None = None


class IngestRequest(BaseModel):
    category: Literal["admissions", "policies", "ciqa", "examination", "syllabus"]
    source: str = Field(..., description="Logical document name / path")
