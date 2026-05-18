import aiohttp
import xml.etree.ElementTree as ET
from typing import List
from app.plugins.base import SearchPlugin, SearchResult, PluginInfo
from app.core.cache import SearchCache


class arXivPlugin(SearchPlugin):
    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self):
        self.cache = SearchCache()

    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="arxiv",
            display_name="arXiv",
            description="Search academic preprints across physics, math, CS, and more",
            category="academic",
            requires_auth=False,
            default_enabled=True,
        )

    @staticmethod
    def _ns(tag: str) -> str:
        return f"{{http://www.w3.org/2005/Atom}}{tag}"

    async def search(self, query: str, limit: int = 20) -> List[SearchResult]:
        cached = self.cache.get("arxiv", query)
        if cached:
            return [SearchResult(**r) for r in cached]

        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": min(limit, 50),
            "sortBy": "relevance",
        }
        results = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.BASE_URL, params=params, timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status != 200:
                        return []
                    text = await resp.text()

            root = ET.fromstring(text)
            for entry in root.findall(self._ns("entry")):
                title_el = entry.find(self._ns("title"))
                summary_el = entry.find(self._ns("summary"))
                title = title_el.text.strip() if title_el is not None and title_el.text else ""
                summary = summary_el.text.strip() if summary_el is not None and summary_el.text else ""

                authors = []
                for author in entry.findall(self._ns("author")):
                    name_el = author.find(self._ns("name"))
                    if name_el is not None and name_el.text:
                        authors.append(name_el.text.strip())

                url_el = entry.find(self._ns("id"))
                url = url_el.text.strip() if url_el is not None and url_el.text else ""

                published_el = entry.find(self._ns("published"))
                published = published_el.text.strip()[:10] if published_el is not None and published_el.text else None

                results.append(SearchResult(
                    source="arxiv",
                    source_url=url,
                    title=title,
                    summary=summary[:2000],
                    authors=authors,
                    published_date=published,
                    url=url,
                    metadata={},
                    relevance_score=0.8,
                ))
        except Exception:
            return []

        dict_results = []
        for r in results:
            d = r.__dict__.copy()
            dict_results.append(d)

        if results:
            self.cache.set("arxiv", query, dict_results)

        return results
