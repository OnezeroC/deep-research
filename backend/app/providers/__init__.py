from app.config import settings
from app.providers.base import BaseProvider
from app.providers.anthropic import AnthropicProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.deepseek import DeepSeekProvider
from app.providers.openai_compatible import OpenAICompatibleProvider


def create_provider() -> BaseProvider:
    provider_name = settings.ai_provider
    match provider_name:
        case "anthropic":
            return AnthropicProvider()
        case "openai":
            return OpenAIProvider()
        case "deepseek":
            return DeepSeekProvider()
        case "openai_compatible":
            return OpenAICompatibleProvider()
        case _:
            raise ValueError(f"Unknown AI provider: {provider_name}. Supported: anthropic, openai, deepseek, openai_compatible")
