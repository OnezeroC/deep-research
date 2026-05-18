from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional, Literal


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8765

    database_url: str = "sqlite+aiosqlite:///./data/deep_research.db"
    data_dir: Path = Path("data")

    # AI Provider — which service to use for analysis
    ai_provider: Literal["anthropic", "openai", "deepseek", "openai_compatible"] = "anthropic"

    # Anthropic
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-sonnet-4-6-20250514"
    anthropic_max_tokens: int = 64000
    anthropic_thinking_budget: int = 16000

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4.1"
    openai_max_tokens: int = 16000
    openai_base_url: Optional[str] = None

    # DeepSeek (OpenAI-compatible)
    deepseek_api_key: Optional[str] = None
    deepseek_model: str = "deepseek-chat"
    deepseek_max_tokens: int = 16000

    # Generic OpenAI-compatible endpoint (Ollama, vLLM, local models, etc.)
    openai_compatible_api_key: Optional[str] = None
    openai_compatible_model: str = "default"
    openai_compatible_base_url: str = "http://localhost:11434/v1"
    openai_compatible_max_tokens: int = 16000

    search_limit_per_source: int = 20
    search_timeout_seconds: float = 60.0
    max_concurrent_searches: int = 5

    cache_ttl_hours: int = 24
    cache_dir: Path = Path("data/cache")

    plugins_enabled: list[str] = ["arxiv", "semantic_scholar", "reddit", "web_search"]

    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    reddit_user_agent: str = "deep-research-tool/1.0"

    output_dir: Path = Path("data/output")

    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
