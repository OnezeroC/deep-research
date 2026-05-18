import aiosqlite
import json
from pathlib import Path
from app.config import settings

DB_PATH = settings.data_dir / "deep_research.db"


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS research_tasks (
    id TEXT PRIMARY KEY,
    query TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    progress REAL DEFAULT 0.0,
    progress_message TEXT,
    plugins_used TEXT,
    search_results TEXT,
    analysis_raw TEXT,
    analysis_structured TEXT,
    error TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS plugin_configs (
    name TEXT PRIMARY KEY,
    enabled INTEGER NOT NULL DEFAULT 1,
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS search_cache (
    id TEXT PRIMARY KEY,
    plugin TEXT NOT NULL,
    query_hash TEXT NOT NULL,
    results TEXT NOT NULL,
    cached_at TEXT NOT NULL DEFAULT (datetime('now')),
    expires_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_search_cache_query
    ON search_cache(plugin, query_hash);

CREATE TABLE IF NOT EXISTS output_cache (
    task_id TEXT NOT NULL,
    format TEXT NOT NULL,
    file_path TEXT,
    generated_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (task_id, format),
    FOREIGN KEY (task_id) REFERENCES research_tasks(id) ON DELETE CASCADE
);
"""


async def init_db():
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.cache_dir.mkdir(parents=True, exist_ok=True)
    settings.output_dir.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.executescript(SCHEMA_SQL)
        await db.commit()


async def get_db():
    db = await aiosqlite.connect(str(DB_PATH))
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    return db
