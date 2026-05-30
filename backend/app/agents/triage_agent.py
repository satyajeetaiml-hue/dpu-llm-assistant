"""Triage agent: routes an incoming message to the right specialist agent."""
from __future__ import annotations

from app.agents.admission_agent import AdmissionAgent
from app.agents.base import AgentReply, BaseAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.marketing_agent import MarketingAgent
from app.agents.student_agent import StudentAgent
from app.core.logging import get_logger
from app.rag.prompts import TRIAGE_SYSTEM
from app.services.azure_foundry import get_foundry_client

logger = get_logger(__name__)

_VALID_INTENTS = {"student", "admission", "compliance", "marketing"}


class TriageAgent:
    """Classifies intent, then delegates to a specialist agent."""

    def __init__(self) -> None:
        self._client = get_foundry_client()
        self._agents: dict[str, BaseAgent] = {
            "student": StudentAgent(),
            "admission": AdmissionAgent(),
            "compliance": ComplianceAgent(),
            "marketing": MarketingAgent(),
        }

    def classify(self, message: str) -> str:
        """Return one of the valid intent labels (defaults to ``student``)."""
        messages = [
            {"role": "system", "content": TRIAGE_SYSTEM},
            {"role": "user", "content": message},
        ]
        raw = self._client.complete_text(
            messages, temperature=0.0, max_tokens=8
        ).strip().lower()
        intent = raw.split()[0] if raw else "student"
        if intent not in _VALID_INTENTS:
            logger.warning("Unrecognised intent '%s', defaulting to student", raw)
            intent = "student"
        return intent

    def handle(
        self,
        message: str,
        *,
        history: list[dict] | None = None,
        forced_agent: str | None = None,
    ) -> AgentReply:
        intent = forced_agent if forced_agent in _VALID_INTENTS else self.classify(
            message
        )
        logger.info("Routing message to '%s' agent", intent)
        return self._agents[intent].answer(message, history=history)


_triage: TriageAgent | None = None


def get_triage_agent() -> TriageAgent:
    """Lazily construct a shared triage agent instance."""
    global _triage
    if _triage is None:
        _triage = TriageAgent()
    return _triage
