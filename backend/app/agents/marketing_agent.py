"""Marketing & outreach agent."""
from __future__ import annotations

from app.agents.base import BaseAgent
from app.rag.prompts import MARKETING_SYSTEM


class MarketingAgent(BaseAgent):
    name = "marketing"
    system_prompt = MARKETING_SYSTEM
    category = None
    temperature = 0.5  # a little more creative for promotional copy
