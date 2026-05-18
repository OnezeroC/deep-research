from fastapi import APIRouter
from app.config import settings

router = APIRouter()


@router.get("/config")
async def get_config():
    return {
        "ai_provider": settings.ai_provider,
        "providers": {
            "anthropic": {
                "model": settings.anthropic_model,
                "max_tokens": settings.anthropic_max_tokens,
                "has_key": bool(settings.anthropic_api_key),
            },
            "openai": {
                "model": settings.openai_model,
                "max_tokens": settings.openai_max_tokens,
                "base_url": settings.openai_base_url,
                "has_key": bool(settings.openai_api_key),
            },
            "deepseek": {
                "model": settings.deepseek_model,
                "max_tokens": settings.deepseek_max_tokens,
                "has_key": bool(settings.deepseek_api_key),
            },
            "openai_compatible": {
                "model": settings.openai_compatible_model,
                "max_tokens": settings.openai_compatible_max_tokens,
                "base_url": settings.openai_compatible_base_url,
                "has_key": bool(settings.openai_compatible_api_key),
            },
        },
    }
