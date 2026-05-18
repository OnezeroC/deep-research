from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.config import settings

router = APIRouter()


@router.get("/research/{task_id}/output.{format}")
async def download_output(task_id: str, format: str):
    if format not in ("md", "tex", "pdf"):
        raise HTTPException(status_code=400, detail="Unsupported format. Use md, tex, or pdf")

    file_path = settings.output_dir / task_id / f"report.{format}"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found. The task may not be complete yet.")

    media_types = {
        "md": "text/markdown",
        "tex": "application/x-latex",
        "pdf": "application/pdf",
    }

    filename = f"report.{format}"
    return FileResponse(
        path=str(file_path),
        media_type=media_types.get(format, "application/octet-stream"),
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
