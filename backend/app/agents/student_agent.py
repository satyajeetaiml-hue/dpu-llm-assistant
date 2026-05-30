"""Student services agent."""
from __future__ import annotations

from app.agents.base import BaseAgent
from app.rag.prompts import STUDENT_SYSTEM


class StudentAgent(BaseAgent):
    name = "student"
    system_prompt = STUDENT_SYSTEM
    category = None  # students may ask across categories
