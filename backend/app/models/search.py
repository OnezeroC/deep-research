from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SearchResult(BaseModel):
    source: str
    source_url: str
    title: str
    summary: str
    authors: list[str] = Field(default_factory=list)
    published_date: Optional[str] = None
    url: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
    relevance_score: float = 0.0


class PluginInfo(BaseModel):
    name: str
    display_name: str
    description: str
    category: str
    requires_auth: bool = False
    default_enabled: bool = True


class PluginConfig(BaseModel):
    name: str
    enabled: bool = True
    config: dict = Field(default_factory=dict)
