import json
import asyncio
import logging
from typing import Callable, Awaitable, Optional, List
from app.config import settings
from app.database import get_db
from app.plugins.registry import PluginRegistry
from app.services.searcher import Searcher
from app.services.deduplicator import Deduplicator
from app.services.analyzer import Analyzer
from app.services.output_generator import OutputGenerator

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, registry: PluginRegistry):
        self.registry = registry
        self.searcher = Searcher()
        self.deduplicator = Deduplicator()
        self.analyzer = Analyzer()
        self.generator = OutputGenerator()

    async def execute(
        self,
        task_id: str,
        query: str,
        plugins: list[str],
        output_formats: list[str],
        progress_callback: Optional[Callable[[dict], Awaitable[None]]] = None,
    ):
        db = await get_db()
        try:
            # Phase 1: Search
            await self._update_task(db, task_id, "searching", 0.1, "Initializing search plugins...")
            await self._emit(progress_callback, "searching", 0.1, "Initializing search plugins...")

            enabled = plugins or settings.plugins_enabled
            await self.registry.discover(enabled)

            await self._update_task(db, task_id, "searching", 0.15, f"Searching across {len(self.registry.get_all())} sources...")
            await self._emit(progress_callback, "searching", 0.15, f"Searching across {len(self.registry.get_all())} sources...")

            all_results = await self.searcher.search_all(query, self.registry)

            await self._update_task(db, task_id, "searching", 0.35,
                                    f"Found {len(all_results)} results. Deduplicating...")
            await self._emit(progress_callback, "searching", 0.35,
                            f"Found {len(all_results)} total results")

            # Phase 2: Dedup
            deduped = self.deduplicator.deduplicate(all_results)

            await self._update_task(db, task_id, "analyzing", 0.4,
                                    f"Deduplicated to {len(deduped)} unique results. Starting AI analysis...")
            await self._emit(progress_callback, "analyzing", 0.4,
                            f"Deduplicated to {len(deduped)} unique results. Starting AI analysis...")

            # Store search results
            results_json = json.dumps([r.__dict__ for r in deduped], ensure_ascii=False)
            await db.execute(
                "UPDATE research_tasks SET search_results = ? WHERE id = ?",
                (results_json, task_id)
            )
            await db.commit()
            await self._emit(progress_callback, "analyzing", 0.45, "Sending to Claude for deep analysis...")

            # Phase 3: Analyze
            analysis = await self.analyzer.analyze(query, deduped)

            analysis_json = json.dumps(analysis, ensure_ascii=False)
            await db.execute(
                "UPDATE research_tasks SET analysis_structured = ? WHERE id = ?",
                (analysis_json, task_id)
            )
            await db.commit()

            await self._update_task(db, task_id, "generating", 0.7, "Generating output files...")
            await self._emit(progress_callback, "generating", 0.7, "Generating reports...")

            # Phase 4: Generate
            await self.generator.generate(task_id, query, analysis, deduped, output_formats)

            await self._update_task(db, task_id, "done", 1.0, "Complete!")
            await self._emit(progress_callback, "done", 1.0, "Research complete!")

            await db.execute(
                "UPDATE research_tasks SET completed_at = datetime('now'), plugins_used = ? WHERE id = ?",
                (json.dumps(enabled), task_id)
            )
            await db.commit()

        except Exception as e:
            logger.exception(f"Research task {task_id} failed")
            await self._update_task(db, task_id, "failed", 0.0, str(e))
            await self._emit(progress_callback, "error", 0.0, str(e))
            await db.execute(
                "UPDATE research_tasks SET error = ? WHERE id = ?",
                (str(e), task_id)
            )
            await db.commit()
        finally:
            await self._update_task(db, task_id, status=None, progress=None, progress_message=None, final=True)

    async def _update_task(self, db, task_id, status=None, progress=None, progress_message=None, final=False):
        sets = []
        vals = []
        if status:
            sets.append("status = ?"); vals.append(status)
        if progress is not None:
            sets.append("progress = ?"); vals.append(progress)
        if progress_message:
            sets.append("progress_message = ?"); vals.append(progress_message)
        if sets:
            sets.append("updated_at = datetime('now')")
            vals.append(task_id)
            await db.execute(f"UPDATE research_tasks SET {', '.join(sets)} WHERE id = ?", vals)
            if not final:
                await db.commit()

    @staticmethod
    async def _emit(cb, phase, progress, message):
        if cb:
            await cb({"phase": phase, "progress": progress, "message": message})
