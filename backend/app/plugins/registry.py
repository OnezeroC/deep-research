import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional
from app.plugins.base import SearchPlugin, PluginInfo
from app.config import settings


class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, SearchPlugin] = {}

    async def discover(self, enabled_list: List[str] | None = None):
        if enabled_list is None:
            enabled_list = None  # None means "all plugins"

        import app.plugins as pkg
        pkg_dir = Path(__file__).parent
        for _, name, _ in pkgutil.iter_modules([str(pkg_dir)]):
            if name in ("base", "registry"):
                continue
            mod = importlib.import_module(f"app.plugins.{name}")
            for attr in dir(mod):
                obj = getattr(mod, attr)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, SearchPlugin)
                    and obj is not SearchPlugin
                ):
                    instance = obj()
                    plugin_name = instance.info.name
                    if plugin_name in self._plugins:
                        continue  # Already registered
                    if enabled_list is None or plugin_name in enabled_list:
                        self._plugins[plugin_name] = instance

    def get(self, name: str) -> Optional[SearchPlugin]:
        return self._plugins.get(name)

    def get_all(self) -> List[SearchPlugin]:
        return list(self._plugins.values())

    def list_plugins(self) -> List[PluginInfo]:
        return [p.info for p in self._plugins.values()]

    async def close_all(self) -> None:
        for p in self._plugins.values():
            await p.close()
