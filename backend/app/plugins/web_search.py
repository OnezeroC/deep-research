import aiohttp
import re
from typing import List
from app.plugins.base import SearchPlugin, SearchResult, PluginInfo
from app.core.cache import SearchCache


class WebSearchPlugin(SearchPlugin):
    SEARCH_URL = "https://api.duckduckgo.com/"

    def __init__(self):
        self.cache = SearchCache()

    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="web_search",
            display_name="Web Search",
            description="Search the web for research-related articles, blogs, and news",
            category="web",
            requires_auth=False,
            default_enabled=True,
        )

    @staticmethod
    def _strip_html(text: str) -> str:
        return re.sub(r"<[^>]+>", "", text)

    async def search(self, query: str, limit: int = 20) -> List[SearchResult]:
        cached = self.cache.get("web_search", query)
        if cached:
            return [SearchResult(**r) for r in cached]

        params = {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1",
            "t": "deep-research-tool",
        }
        results = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.SEARCH_URL, params=params,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status != 200:
                        return []
                    data = await resp.json()

            abstract = data.get("Abstract", "")
            abstract_url = data.get("AbstractURL", "")
            abstract_source = data.get("AbstractSource", "")
            heading = data.get("Heading", "")

            if abstract and heading:
                results.append(SearchResult(
                    source="web_search",
                    source_url=abstract_url or "",
                    title=heading,
                    summary=abstract[:2000],
                    authors=[abstract_source] if abstract_source else [],
                    url=abstract_url,
                    metadata={"type": "abstract"},
                    relevance_score=0.9,
                ))

            for topic in data.get("RelatedTopics", [])[:limit - 1]:
                if isinstance(topic, dict):
                    text = topic.get("Text", "")
                    url = topic.get("FirstURL", "")
                    results.append(SearchResult(
                        source="web_search",
                        source_url=url,
                        title=text[:200] if text else "",
                        summary=self._strip_html(text)[:2000],
                        url=url,
                        metadata={"type": "related"},
                        relevance_score=0.5,
                    ))

            for result in data.get("Results", [])[:limit - len(results)]:
                rtext = result.get("Text", "")
                rurl = result.get("FirstURL", "")
                if rtext and rurl:
                    results.append(SearchResult(
                        source="web_search",
                        source_url=rurl,
                        title=rtext[:200],
                        summary=self._strip_html(rtext)[:2000],
                        url=rurl,
                        metadata={"type": "web_result"},
                        relevance_score=0.4,
                    ))
        except Exception:
            return []

        dict_results = [r.__dict__ for r in results]
        if results:
            self.cache.set("web_search", query, dict_results)
        return results
