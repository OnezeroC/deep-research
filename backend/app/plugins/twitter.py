import aiohttp
from typing import List
from app.plugins.base import SearchPlugin, SearchResult, PluginInfo
from app.core.cache import SearchCache


class TwitterXPlugin(SearchPlugin):
    NITTER_INSTANCES = [
        "https://nitter.net",
        "https://nitter.privacydev.net",
    ]

    def __init__(self):
        self.cache = SearchCache()

    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="twitter",
            display_name="Twitter / X",
            description="Search real-time research discussions on Twitter/X (experimental)",
            category="social",
            requires_auth=False,
            default_enabled=False,
        )

    async def search(self, query: str, limit: int = 20) -> List[SearchResult]:
        cached = self.cache.get("twitter", query)
        if cached:
            return [SearchResult(**r) for r in cached]

        results = []
        for instance in self.NITTER_INSTANCES:
            if len(results) >= limit:
                break
            try:
                search_url = f"{instance}/search"
                params = {"f": "tweets", "q": query}
                headers = {"User-Agent": "deep-research-tool/1.0"}
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        search_url, params=params, headers=headers,
                        timeout=aiohttp.ClientTimeout(total=20)
                    ) as resp:
                        if resp.status != 200:
                            continue
                        html = await resp.text()

                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, "html.parser")
                for item in soup.select(".timeline-item")[:limit]:
                    content_el = item.select_one(".tweet-content")
                    date_el = item.select_one(".tweet-date a")
                    author_el = item.select_one(".fullname")
                    link_el = item.select_one(".tweet-link")

                    text = content_el.get_text(strip=True) if content_el else ""
                    if not text:
                        continue

                    results.append(SearchResult(
                        source="twitter",
                        source_url=link_el.get("href", "") if link_el else "",
                        title=text[:200],
                        summary=text[:2000],
                        authors=[author_el.get_text(strip=True)] if author_el else [],
                        published_date=date_el.get("title", "") if date_el else None,
                        url=link_el.get("href", "") if link_el else None,
                        metadata={"platform": "twitter"},
                        relevance_score=0.3,
                    ))
                if results:
                    break  # Successfully got results from this instance
            except Exception:
                continue

        dict_results = [r.__dict__ for r in results]
        if results:
            self.cache.set("twitter", query, dict_results, ttl_hours=12)
        return results
