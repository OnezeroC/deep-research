import asyncio
import shutil
from pathlib import Path
from app.config import settings


class PdfRenderer:
    async def render(self, task_id: str) -> Path:
        output_dir = settings.output_dir / task_id
        md_path = output_dir / "report.md"
        pdf_path = output_dir / "report.pdf"

        if not md_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {md_path}")

        pandoc = shutil.which("pandoc")
        if not pandoc:
            raise RuntimeError("pandoc not found. Install it: brew install pandoc")

        cmd = [
            pandoc,
            str(md_path),
            "-o", str(pdf_path),
            "--pdf-engine=pdflatex",
            "--from=markdown+smart",
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
        except asyncio.TimeoutError:
            proc.kill()
            raise RuntimeError("pandoc timed out after 120s")

        if proc.returncode != 0:
            err = stderr.decode() if stderr else "unknown error"
            raise RuntimeError(f"pandoc failed (exit {proc.returncode}): {err[:500]}")

        return pdf_path
