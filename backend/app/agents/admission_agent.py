"""Admissions agent."""
from __future__ import annotations

from app.agents.base import BaseAgent
from app.rag.prompts import ADMISSION_SYSTEM


class AdmissionAgent(BaseAgent):
    name = "admission"
    system_prompt = ADMISSION_SYSTEM
    category = "admissions"
