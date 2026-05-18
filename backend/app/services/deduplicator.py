import re
from typing import List
from app.plugins.base import SearchResult


class Deduplicator:
    def deduplicate(self, results: List[SearchResult]) -> List[SearchResult]:
        if not results:
            return []

        seen_urls: set[str] = set()
        seen_titles: set[str] = set()
        unique: List[SearchResult] = []

        for r in results:
            url_key = (r.url or "").strip().lower().rstrip("/")
            if url_key and url_key in seen_urls:
                continue

            title_key = self._normalize_title(r.title)
            if title_key in seen_titles:
                continue

            if url_key:
                seen_urls.add(url_key)
            seen_titles.add(title_key)
            unique.append(r)

        return unique

    @staticmethod
    def _normalize_title(title: str) -> str:
        t = title.lower().strip()
        t = re.sub(r"[^a-z0-9\s]", "", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t
