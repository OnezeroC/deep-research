import aiohttp
from typing import List
from app.plugins.base import SearchPlugin, SearchResult, PluginInfo
from app.core.cache import SearchCache


class RedditPlugin(SearchPlugin):
    SEARCH_URL = "https://old.reddit.com/search.json"

    def __init__(self):
        self.cache = SearchCache()

    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="reddit",
            display_name="Reddit",
            description="Search research-related discussions and communities on Reddit",
            category="social",
            requires_auth=False,
            default_enabled=True,
        )

    async def search(self, query: str, limit: int = 20) -> List[SearchResult]:
        cached = self.cache.get("reddit", query)
        if cached:
            return [SearchResult(**r) for r in cached]

        headers = {"User-Agent": "deep-research-tool/1.0"}
        params = {"q": query, "limit": min(limit, 100), "sort": "relevance", "t": "year"}
        results = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.SEARCH_URL, params=params, headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status != 200:
                        return []
                    data = await resp.json()

            for child in data.get("data", {}).get("children", []):
                post = child.get("data", {})
                title = post.get("title", "")
                selftext = post.get("selftext", "")
                summary = selftext[:2000] if selftext else title
                permalink = post.get("permalink", "")
                url = f"https://old.reddit.com{permalink}" if permalink else ""
                created_utc = post.get("created_utc")

                from datetime import datetime
                published = None
                if created_utc:
                    published = datetime.utcfromtimestamp(created_utc).strftime("%Y-%m-%d")

                results.append(SearchResult(
                    source="reddit",
                    source_url=url,
                    title=title[:500],
                    summary=summary,
                    authors=[post.get("author", "unknown")],
                    published_date=published,
                    url=url,
                    metadata={
                        "subreddit": post.get("subreddit", ""),
                        "score": post.get("score", 0),
                        "num_comments": post.get("num_comments", 0),
                    },
                    relevance_score=min(1.0, post.get("score", 0) / 100),
                ))
        except Exception:
            return []

        dict_results = [r.__dict__ for r in results]
        if results:
            self.cache.set("reddit", query, dict_results)
        return results
