"""Chat endpoint: routes a user message through the triage agent."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.agents.triage_agent import get_triage_agent
from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse
from app.services.auth import get_current_user

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: dict[str, Any] = Depends(get_current_user),
) -> ChatResponse:
    history = [m.model_dump() for m in request.history]
    reply = get_triage_agent().handle(
        request.message,
        history=history,
        forced_agent=request.agent,
    )
    return ChatResponse(
        answer=reply.answer,
        agent=reply.agent,
        citations=reply.citations,
        session_id=request.session_id,
    )
