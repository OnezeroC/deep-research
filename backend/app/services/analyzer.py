import json
import logging
from typing import List
from app.config import settings
from app.plugins.base import SearchResult
from app.providers import create_provider
from app.providers.base import BaseProvider

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert research analyst. Your task is to synthesize information from multiple sources into a comprehensive research landscape report.

You will receive:
1. A research topic/question
2. Search results from academic journals, social media platforms, and the web

Produce a structured analysis in the following JSON format:

{
  "executive_summary": "2-3 paragraph overview of the current state of this field",
  "research_hotspots": [
    {"topic": "...", "intensity": "high|medium|low", "description": "...", "key_sources": [0, 3, 5]}
  ],
  "key_innovations": [
    {"innovation": "...", "year": 2024, "significance": "...", "source_indices": [1, 2]}
  ],
  "historical_context": {
    "timeline": [
      {"year": 2018, "event": "...", "significance": "..."}
    ],
    "narrative": "..."
  },
  "key_papers_and_discussions": [
    {"title": "...", "source": "arxiv|reddit|web_search|semantic_scholar|...", "url": "...", "why_important": "..."}
  ],
  "methodologies_and_approaches": [
    {"name": "...", "description": "...", "maturity": "established|emerging|experimental"}
  ],
  "controversies_and_debates": [
    {"topic": "...", "summary": "...", "source_indices": [4, 7]}
  ],
  "emerging_trends": [
    {"trend": "...", "confidence": "high|medium|low", "evidence": "..."}
  ],
  "gaps_and_opportunities": [
    {"gap": "...", "opportunity": "..."}
  ],
  "recommended_reading": [
    {"title": "...", "url": "...", "priority": 1}
  ],
  "search_quality_assessment": "Assessment of whether results were sufficient"
}

Source indices refer to the numbered list of search results provided.
If a section has no relevant content, use an empty list, never omit keys.
All text should be in English. If the topic is in Chinese, translate to English first."""


class Analyzer:
    def __init__(self):
        self._provider: BaseProvider | None = None

    def _get_provider(self) -> BaseProvider:
        if self._provider is None:
            self._provider = create_provider()
        return self._provider

    def _get_max_tokens(self) -> int:
        provider_name = settings.ai_provider
        match provider_name:
            case "anthropic":
                return settings.anthropic_max_tokens
            case "openai":
                return settings.openai_max_tokens
            case "deepseek":
                return settings.deepseek_max_tokens
            case "openai_compatible":
                return settings.openai_compatible_max_tokens
            case _:
                return 16000

    def _format_results(self, results: List[SearchResult]) -> str:
        lines = []
        for i, r in enumerate(results):
            authors = ", ".join(r.authors[:3])
            date_str = f" ({r.published_date})" if r.published_date else ""
            lines.append(
                f"[{i}] [{r.source.upper()}]{date_str} {r.title}\n"
                f"    Authors: {authors or 'N/A'}\n"
                f"    Summary: {r.summary[:500]}\n"
                f"    URL: {r.url or r.source_url}"
            )
        return "\n\n".join(lines)

    @staticmethod
    def _repair_json(text: str) -> str:
        """Fix common LLM JSON mistakes."""
        import re
        # Remove trailing commas before ] or }
        text = re.sub(r",\s*(\]|\})", r"\1", text)
        # Remove commas before newline + } or ]
        text = re.sub(r",(\s*\n\s*[\}\]])", r"\1", text)
        # Fix year ranges: "year": 2019-2020 -> "year": "2019-2020"
        text = re.sub(r'("year"\s*:\s*)(\d{4})\s*-\s*(\d{4})', r'\1"\2-\3"', text)
        return text

    def _extract_json(self, text: str) -> dict:
        text = text.strip()
        extract_attempts = [text]

        if "```json" in text:
            try:
                start = text.index("```json") + 7
                end = text.index("```", start)
                extract_attempts.insert(0, text[start:end].strip())
            except (ValueError, IndexError):
                pass

        if "```" in text:
            try:
                start = text.index("```") + 3
                end = text.index("```", start)
                extract_attempts.insert(0, text[start:end].strip())
            except (ValueError, IndexError):
                pass

        first_brace = text.find("{")
        last_brace = text.rfind("}")
        if first_brace >= 0 and last_brace > first_brace:
            extract_attempts.insert(0, text[first_brace:last_brace + 1])

        for attempt in extract_attempts:
            try:
                return json.loads(attempt)
            except json.JSONDecodeError:
                pass
            # Try repaired version
            try:
                return json.loads(self._repair_json(attempt))
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Could not parse JSON from response: {text[:300]}...")

    async def analyze(self, query: str, results: List[SearchResult]) -> dict:
        formatted = self._format_results(results)
        max_index = len(results) - 1

        user_message = f"""Research Topic: {query}

Below are {len(results)} search results collected from multiple platforms.
Each result is numbered [0] through [{max_index}].

{formatted}

Please provide your structured analysis of the research landscape for this topic."""

        provider = self._get_provider()
        logger.info(f"Sending {len(results)} results to {provider.name} for analysis")

        text = await provider.analyze(SYSTEM_PROMPT, user_message, self._get_max_tokens())

        if not text:
            raise ValueError(f"{provider.name} returned no text content")

        # Save raw response for debugging
        self._last_raw = text

        return self._extract_json(text)
