from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    plugins: Optional[list[str]] = None
    output_formats: list[str] = Field(default=["md", "tex", "pdf"])


class ResearchTask(BaseModel):
    id: str
    query: str
    status: str
    progress: float
    progress_message: Optional[str] = None
    plugins_used: Optional[list[str]] = None
    search_results: Optional[list] = None
    analysis_raw: Optional[str] = None
    analysis_structured: Optional[dict] = None
    error: Optional[str] = None
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None


class ResearchListResponse(BaseModel):
    tasks: list[ResearchTask]
    total: int
