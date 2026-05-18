from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from app.config import settings


class MarkdownRenderer:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(Path(__file__).parent / "templates"),
            autoescape=False,
        )

    def render(
        self,
        query: str,
        analysis: dict,
        total_results: int,
        sources: list[str],
        generated_at: str,
    ) -> str:
        template = self.env.get_template("report.md.j2")
        return template.render(
            query=query,
            analysis=analysis,
            total_results=total_results,
            sources=sources,
            model=settings.anthropic_model,
            generated_at=generated_at,
        )
