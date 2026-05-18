import logging
from openai import AsyncOpenAI
from app.config import settings
from app.providers.base import BaseProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseProvider):
    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url or None,
        )
        self.model = settings.openai_model

    @property
    def name(self) -> str:
        return "openai"

    async def analyze(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        logger.info(f"Calling OpenAI API (model: {self.model})")
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
