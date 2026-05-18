import json
import logging
from fastapi import APIRouter
from app.database import get_db
from app.plugins.registry import PluginRegistry
from app.plugins.base import PluginInfo

logger = logging.getLogger(__name__)
router = APIRouter()

_registry: PluginRegistry | None = None


def get_registry() -> PluginRegistry:
    global _registry
    if _registry is None:
        _registry = PluginRegistry()
    return _registry


@router.get("/plugins")
async def list_plugins():
    registry = get_registry()
    db = await get_db()
    try:
        # Get config overrides from DB
        configs: dict[str, dict] = {}
        async with db.execute("SELECT * FROM plugin_configs") as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                configs[row["name"]] = {
                    "enabled": bool(row["enabled"]),
                    "config": json.loads(row["config_json"]) if row["config_json"] else {},
                }

        # Discover all plugins from registry
        await registry.discover(None)
        all_infos = registry.list_plugins()

        plugins = []
        for info in all_infos:
            db_config = configs.get(info.name, {})
            plugins.append({
                "name": info.name,
                "display_name": info.display_name,
                "description": info.description,
                "category": info.category,
                "requires_auth": info.requires_auth,
                "default_enabled": info.default_enabled,
                "enabled": db_config.get("enabled", info.default_enabled),
                "config": db_config.get("config", {}),
            })
        return {"plugins": plugins}
    finally:
        await db.close()


@router.put("/plugins/{name}/config")
async def configure_plugin(name: str, body: dict):
    db = await get_db()
    try:
        enabled = body.get("enabled", True)
        config_json = json.dumps(body.get("config", {}))

        await db.execute(
            """INSERT INTO plugin_configs (name, enabled, config_json, updated_at)
               VALUES (?, ?, ?, datetime('now'))
               ON CONFLICT(name) DO UPDATE SET
               enabled = excluded.enabled,
               config_json = excluded.config_json,
               updated_at = excluded.updated_at""",
            (name, int(enabled), config_json)
        )
        await db.commit()

        return {
            "name": name,
            "enabled": enabled,
            "config": body.get("config", {}),
        }
    finally:
        await db.close()
