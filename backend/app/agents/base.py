"""Base class shared by all RAG agents."""
from __future__ import annotations

from dataclasses import dataclass, field

from app.models.response_models import Citation
from app.rag.prompts import build_rag_messages
from app.rag.retrieval import RetrievedPassage, format_context, retrieve
from app.services.azure_foundry import get_foundry_client


@dataclass
class AgentReply:
    answer: str
    agent: str
    citations: list[Citation] = field(default_factory=list)


class BaseAgent:
    """A grounded agent: retrieve context, then answer with Azure AI Foundry.

    Subclasses set ``name``, ``system_prompt`` and (optionally) ``category`` to
    scope retrieval to a document category.
    """

    name: str = "base"
    system_prompt: str = ""
    category: str | None = None
    temperature: float = 0.2

    def __init__(self) -> None:
        self._client = get_foundry_client()

    def _citations(self, passages: list[RetrievedPassage]) -> list[Citation]:
        return [
            Citation(
                index=i,
                source=p.source,
                category=p.category,
                page=p.page,
            )
            for i, p in enumerate(passages, start=1)
        ]

    def answer(
        self, question: str, history: list[dict] | None = None
    ) -> AgentReply:
        passages = retrieve(question, category=self.category)
        context = format_context(passages)
        messages = build_rag_messages(
            system_prompt=self.system_prompt,
            context=context,
            question=question,
            history=history,
        )
        text = self._client.complete_text(messages, temperature=self.temperature)
        return AgentReply(
            answer=text,
            agent=self.name,
            citations=self._citations(passages),
        )
