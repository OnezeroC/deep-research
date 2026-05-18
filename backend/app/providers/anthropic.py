import logging
from anthropic import AsyncAnthropic
from app.config import settings
from app.providers.base import BaseProvider

logger = logging.getLogger(__name__)


class AnthropicProvider(BaseProvider):
    def __init__(self):
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        self.model = settings.anthropic_model
        self.thinking_budget = settings.anthropic_thinking_budget

    @property
    def name(self) -> str:
        return "anthropic"

    async def analyze(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        logger.info(f"Calling Anthropic API (model: {self.model})")
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            thinking={"type": "enabled", "budget_tokens": self.thinking_budget},
            messages=[{"role": "user", "content": user_message}],
        )
        return "".join(
            block.text for block in response.content
            if hasattr(block, "text") and block.type == "text"
        )
