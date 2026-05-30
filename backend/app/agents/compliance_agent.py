"""Compliance & quality assurance (CIQA) agent."""
from __future__ import annotations

from app.agents.base import BaseAgent
from app.rag.prompts import COMPLIANCE_SYSTEM


class ComplianceAgent(BaseAgent):
    name = "compliance"
    system_prompt = COMPLIANCE_SYSTEM
    category = "ciqa"
    temperature = 0.0  # be conservative on policy answers
