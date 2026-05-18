import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from app.config import settings


def escape_tex(text: str) -> str:
    if not text:
        return ""
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
        "\\": r"\textbackslash{}",
    }
    for ch, repl in replacements.items():
        text = text.replace(ch, repl)
    return text


class LatexRenderer:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(Path(__file__).parent / "templates"),
            autoescape=False,
        )
        self.env.filters["escape_tex"] = escape_tex

    def render(
        self,
        query: str,
        analysis: dict,
        total_results: int,
        sources: list[str],
        generated_at: str,
    ) -> str:
        template = self.env.get_template("report.tex.j2")
        return template.render(
            query=query,
            analysis=analysis,
            total_results=total_results,
            sources=sources,
            model=settings.anthropic_model,
            generated_at=generated_at,
        )
