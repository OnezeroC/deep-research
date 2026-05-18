import logging
from openai import AsyncOpenAI
from app.config import settings
from app.providers.base import BaseProvider

logger = logging.getLogger(__name__)


class OpenAICompatibleProvider(BaseProvider):
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.openai_compatible_api_key or "not-needed",
            base_url=settings.openai_compatible_base_url,
        )
        self.model = settings.openai_compatible_model

    @property
    def name(self) -> str:
        return "openai_compatible"

    async def analyze(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        logger.info(f"Calling OpenAI-compatible API (model: {self.model}, base_url: {settings.openai_compatible_base_url})")
        response = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=0.3,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content or ""
