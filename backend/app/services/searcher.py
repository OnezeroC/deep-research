import asyncio
import logging
from typing import List
from app.plugins.base import SearchPlugin, SearchResult
from app.plugins.registry import PluginRegistry
from app.config import settings

logger = logging.getLogger(__name__)


class Searcher:
    async def search_all(
        self,
        query: str,
        registry: PluginRegistry,
        limit: int | None = None,
        timeout: float | None = None,
    ) -> List[SearchResult]:
        if limit is None:
            limit = settings.search_limit_per_source
        if timeout is None:
            timeout = settings.search_timeout_seconds

        plugins = registry.get_all()

        async def _search_one(plugin: SearchPlugin) -> List[SearchResult]:
            try:
                result = await asyncio.wait_for(
                    plugin.search(query, limit), timeout=timeout
                )
                logger.info(f"Plugin {plugin.info.name}: {len(result)} results")
                return result
            except asyncio.TimeoutError:
                logger.warning(f"Plugin {plugin.info.name} timed out after {timeout}s")
                return []
            except Exception:
                logger.exception(f"Plugin {plugin.info.name} failed")
                return []

        tasks = [_search_one(p) for p in plugins]
        all_results: List[SearchResult] = []
        for coro in asyncio.as_completed(tasks):
            batch = await coro
            all_results.extend(batch)

        return all_results
