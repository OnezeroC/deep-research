import hashlib
import json
import time
from pathlib import Path
from app.config import settings


class SearchCache:
    def __init__(self):
        self.cache_dir = settings.cache_dir

    @staticmethod
    def _cache_key(plugin: str, query: str) -> str:
        raw = f"{plugin}:{query.lower().strip()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    def get(self, plugin: str, query: str) -> list | None:
        key = self._cache_key(plugin, query)
        cache_file = self.cache_dir / f"{key}.json"
        if not cache_file.exists():
            return None

        try:
            data = json.loads(cache_file.read_text())
            if data.get("expires_at", 0) < time.time():
                cache_file.unlink(missing_ok=True)
                return None
            return data.get("results")
        except (json.JSONDecodeError, KeyError):
            cache_file.unlink(missing_ok=True)
            return None

    def set(self, plugin: str, query: str, results: list, ttl_hours: int | None = None):
        if ttl_hours is None:
            ttl_hours = settings.cache_ttl_hours
        key = self._cache_key(plugin, query)
        cache_file = self.cache_dir / f"{key}.json"
        data = {
            "plugin": plugin,
            "query": query,
            "results": results,
            "cached_at": time.time(),
            "expires_at": time.time() + ttl_hours * 3600,
        }
        cache_file.write_text(json.dumps(data, ensure_ascii=False))
