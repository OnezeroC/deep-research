import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from app.config import settings
from app.database import get_db
from app.output.markdown_renderer import MarkdownRenderer
from app.output.latex_renderer import LatexRenderer
from app.output.pdf_renderer import PdfRenderer

logger = logging.getLogger(__name__)


class OutputGenerator:
    def __init__(self):
        self.md_renderer = MarkdownRenderer()
        self.tex_renderer = LatexRenderer()
        self.pdf_renderer = PdfRenderer()

    async def generate(
        self,
        task_id: str,
        query: str,
        analysis: dict,
        results: list,
        formats: list[str],
    ):
        output_dir = settings.output_dir / task_id
        output_dir.mkdir(parents=True, exist_ok=True)

        sources = list(set(r.source for r in results))
        total_results = len(results)
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        db = await get_db()
        try:
            if "md" in formats:
                md_content = self.md_renderer.render(
                    query, analysis, total_results, sources, generated_at
                )
                md_path = output_dir / "report.md"
                md_path.write_text(md_content, encoding="utf-8")
                await self._cache_output(db, task_id, "md", md_path)

                if "tex" in formats:
                    tex_content = self.tex_renderer.render(
                        query, analysis, total_results, sources, generated_at
                    )
                    tex_path = output_dir / "report.tex"
                    tex_path.write_text(tex_content, encoding="utf-8")
                    await self._cache_output(db, task_id, "tex", tex_path)

                if "pdf" in formats:
                    try:
                        pdf_path = await self.pdf_renderer.render(task_id)
                        await self._cache_output(db, task_id, "pdf", pdf_path)
                    except (FileNotFoundError, RuntimeError) as e:
                        logger.warning(f"PDF generation skipped: {e}")

            elif "tex" in formats:
                tex_content = self.tex_renderer.render(
                    query, analysis, total_results, sources, generated_at
                )
                tex_path = output_dir / "report.tex"
                tex_path.write_text(tex_content, encoding="utf-8")
                await self._cache_output(db, task_id, "tex", tex_path)

            await db.commit()
        finally:
            await db.close()

    @staticmethod
    async def _cache_output(db, task_id, fmt, path):
        await db.execute(
            """INSERT INTO output_cache (task_id, format, file_path, generated_at)
               VALUES (?, ?, ?, datetime('now'))
               ON CONFLICT(task_id, format) DO UPDATE SET
               file_path = excluded.file_path,
               generated_at = excluded.generated_at""",
            (task_id, fmt, str(path))
        )
