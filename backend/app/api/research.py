import json
import uuid
import asyncio
import logging
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from fastapi.responses import StreamingResponse
from app.database import get_db
from app.models.research import ResearchRequest, ResearchTask
from app.plugins.registry import PluginRegistry
from app.services.orchestrator import Orchestrator

logger = logging.getLogger(__name__)
router = APIRouter()

_task_queues: dict[str, asyncio.Queue] = {}
_registry: PluginRegistry | None = None


def _get_registry() -> PluginRegistry:
    global _registry
    if _registry is None:
        _registry = PluginRegistry()
    return _registry


@router.post("/research", status_code=202)
async def create_research(req: ResearchRequest):
    task_id = str(uuid.uuid4())
    queue: asyncio.Queue = asyncio.Queue()
    _task_queues[task_id] = queue

    db = await get_db()
    try:
        plugins_list = req.plugins or []
        await db.execute(
            """INSERT INTO research_tasks (id, query, status, progress, progress_message, plugins_used)
               VALUES (?, ?, 'pending', 0.0, 'Queued...', ?)""",
            (task_id, req.query, json.dumps(plugins_list))
        )
        await db.commit()
    finally:
        await db.close()

    async def progress_callback(event: dict):
        try:
            queue.put_nowait(event)
        except Exception:
            pass

    registry = _get_registry()
    orchestrator = Orchestrator(registry)

    asyncio.create_task(
        orchestrator.execute(
            task_id=task_id,
            query=req.query,
            plugins=plugins_list,
            output_formats=req.output_formats,
            progress_callback=progress_callback,
        )
    )

    return {"task_id": task_id, "status": "pending"}


@router.get("/research/{task_id}")
async def get_research(task_id: str):
    db = await get_db()
    try:
        async with db.execute(
            "SELECT * FROM research_tasks WHERE id = ?", (task_id,)
        ) as cursor:
            row = await cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "task_id": row["id"],
            "query": row["query"],
            "status": row["status"],
            "progress": row["progress"],
            "progress_message": row["progress_message"],
            "plugins_used": json.loads(row["plugins_used"]) if row["plugins_used"] else [],
            "search_results": json.loads(row["search_results"]) if row["search_results"] else None,
            "analysis_raw": row["analysis_raw"],
            "analysis_structured": json.loads(row["analysis_structured"]) if row["analysis_structured"] else None,
            "error": row["error"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "completed_at": row["completed_at"],
        }
    finally:
        await db.close()


@router.get("/research/{task_id}/stream")
async def stream_research(task_id: str, request: Request):
    queue = _task_queues.get(task_id)

    async def event_generator():
        if queue is None:
            yield f"event: error\ndata: {json.dumps({'message': 'Task not found'})}\n\n"
            return

        while True:
            if await request.is_disconnected():
                _task_queues.pop(task_id, None)
                break
            try:
                event = await asyncio.wait_for(queue.get(), timeout=300)
                event_type = event.get("phase", "progress")
                yield f"event: {event_type}\ndata: {json.dumps(event, ensure_ascii=False)}\n\n"
                if event_type in ("done", "error"):
                    _task_queues.pop(task_id, None)
                    break
            except asyncio.TimeoutError:
                yield f"event: error\ndata: {json.dumps({'message': 'Timeout waiting for task'})}\n\n"
                _task_queues.pop(task_id, None)
                break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/research/history")
async def get_history(limit: int = 20, offset: int = 0):
    db = await get_db()
    try:
        async with db.execute(
            "SELECT COUNT(*) as total FROM research_tasks"
        ) as cursor:
            total_row = await cursor.fetchone()
            total = total_row["total"] if total_row else 0

        async with db.execute(
            "SELECT * FROM research_tasks ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset)
        ) as cursor:
            rows = await cursor.fetchall()

        tasks = []
        for row in rows:
            tasks.append({
                "task_id": row["id"],
                "query": row["query"],
                "status": row["status"],
                "progress": row["progress"],
                "progress_message": row["progress_message"],
                "plugins_used": json.loads(row["plugins_used"]) if row["plugins_used"] else [],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "completed_at": row["completed_at"],
                "error": row["error"],
            })

        return {"tasks": tasks, "total": total}
    finally:
        await db.close()


@router.delete("/research/{task_id}", status_code=204)
async def delete_research(task_id: str):
    _task_queues.pop(task_id, None)
    db = await get_db()
    try:
        cursor = await db.execute("DELETE FROM research_tasks WHERE id = ?", (task_id,))
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
    finally:
        await db.close()
