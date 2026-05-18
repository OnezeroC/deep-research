from pydantic import BaseModel
from enum import Enum


class OutputFormat(str, Enum):
    MARKDOWN = "md"
    LATEX = "tex"
    PDF = "pdf"
