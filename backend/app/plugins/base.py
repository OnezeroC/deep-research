from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PluginInfo:
    name: str
    display_name: str
    description: str
    category: str
    requires_auth: bool = False
    default_enabled: bool = True


@dataclass
class SearchResult:
    source: str
    source_url: str
    title: str
    summary: str
    authors: List[str] = field(default_factory=list)
    published_date: Optional[str] = None
    url: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    relevance_score: float = 0.0


class SearchPlugin(ABC):
    @property
    @abstractmethod
    def info(self) -> PluginInfo:
        ...

    @abstractmethod
    async def search(self, query: str, limit: int = 20) -> List[SearchResult]:
        ...

    async def validate_connection(self) -> bool:
        return True

    async def close(self) -> None:
        pass
