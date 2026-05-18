import aiohttp
import json
from typing import List
from app.plugins.base import SearchPlugin, SearchResult, PluginInfo
from app.core.cache import SearchCache


class XiaohongshuPlugin(SearchPlugin):
    SEARCH_URL = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"

    def __init__(self):
        self.cache = SearchCache()

    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="xiaohongshu",
            display_name="Xiaohongshu",
            description="Search Xiaohongshu (小红书) for research-related Chinese discussions (experimental)",
            category="social",
            requires_auth=False,
            default_enabled=False,
        )

    async def search(self, query: str, limit: int = 20) -> List[SearchResult]:
        cached = self.cache.get("xiaohongshu", query)
        if cached:
            return [SearchResult(**r) for r in cached]

        results = []
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Content-Type": "application/json;charset=UTF-8",
                "Origin": "https://www.xiaohongshu.com",
                "Referer": "https://www.xiaohongshu.com/",
            }
            payload = {
                "keyword": query,
                "page": 1,
                "page_size": min(limit, 50),
                "search_id": f"dr_{hash(query) & 0xFFFFFFFF:x}",
                "sort": "general",
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.SEARCH_URL, json=payload, headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status != 200:
                        return []
                    data = await resp.json()

            for note in data.get("data", {}).get("notes", [])[:limit]:
                note_card = note.get("note_card", note)
                display_title = note_card.get("display_title", "")
                desc = note_card.get("desc", "")
                title = display_title or desc[:200]
                summary = desc or display_title
                note_id = note_card.get("note_id", "")
                url = f"https://www.xiaohongshu.com/explore/{note_id}" if note_id else ""
                author_info = note_card.get("user", {})
                author_name = author_info.get("nickname", "") if isinstance(author_info, dict) else ""

                results.append(SearchResult(
                    source="xiaohongshu",
                    source_url=url,
                    title=title,
                    summary=summary[:2000],
                    authors=[author_name] if author_name else [],
                    url=url,
                    metadata={
                        "likes": note_card.get("liked_count", 0),
                        "collects": note_card.get("collected_count", 0),
                        "comments": note_card.get("comments_count", 0),
                        "platform": "xiaohongshu",
                    },
                    relevance_score=0.25,
                ))
        except Exception:
            return []

        dict_results = [r.__dict__ for r in results]
        if results:
            self.cache.set("xiaohongshu", query, dict_results, ttl_hours=12)
        return results
