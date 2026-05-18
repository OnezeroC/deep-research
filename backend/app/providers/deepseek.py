import logging
from openai import AsyncOpenAI
from app.config import settings
from app.providers.base import BaseProvider

logger = logging.getLogger(__name__)


class DeepSeekProvider(BaseProvider):
    BASE_URL = "https://api.deepseek.com/v1"

    def __init__(self):
        if not settings.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY not set")
        self.client = AsyncOpenAI(
            api_key=settings.deepseek_api_key,
            base_url=self.BASE_URL,
        )
        self.model = settings.deepseek_model

    @property
    def name(self) -> str:
        return "deepseek"

    async def analyze(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        logger.info(f"Calling DeepSeek API (model: {self.model})")
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
