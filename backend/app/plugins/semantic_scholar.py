import aiohttp
from typing import List
from app.plugins.base import SearchPlugin, SearchResult, PluginInfo
from app.core.cache import SearchCache


class SemanticScholarPlugin(SearchPlugin):
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def __init__(self):
        self.cache = SearchCache()

    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="semantic_scholar",
            display_name="Semantic Scholar",
            description="Search millions of peer-reviewed research papers with citations",
            category="academic",
            requires_auth=False,
            default_enabled=True,
        )

    async def search(self, query: str, limit: int = 20) -> List[SearchResult]:
        cached = self.cache.get("semantic_scholar", query)
        if cached:
            return [SearchResult(**r) for r in cached]

        params = {
            "query": query,
            "limit": min(limit, 100),
            "fields": "title,abstract,authors,year,url,externalIds",
        }
        results = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.BASE_URL, params=params, timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status != 200:
                        return []
                    data = await resp.json()

            for paper in data.get("data", []):
                authors = [a.get("name", "") for a in paper.get("authors", [])]
                external_ids = paper.get("externalIds", {})
                paper_url = paper.get("url", "")
                doi = external_ids.get("DOI", "")
                source_url = f"https://doi.org/{doi}" if doi else paper_url
                year = paper.get("year")
                published = f"{year}-01-01" if year else None

                results.append(SearchResult(
                    source="semantic_scholar",
                    source_url=source_url or paper_url,
                    title=paper.get("title", ""),
                    summary=(paper.get("abstract") or "")[:2000],
                    authors=authors,
                    published_date=published,
                    url=paper_url,
                    metadata={"doi": doi, "year": year, "external_ids": external_ids},
                    relevance_score=0.85,
                ))
        except Exception:
            return []

        dict_results = []
        for r in results:
            d = r.__dict__.copy()
            dict_results.append(d)

        if results:
            self.cache.set("semantic_scholar", query, dict_results)

        return results
