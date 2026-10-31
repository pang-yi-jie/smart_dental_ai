"""文件存储：图片保存与路径管理。"""

import shutil
from pathlib import Path

from fastapi import UploadFile

from app.config import settings


def save_upload(file: UploadFile, assessment_id: int, kind: str = "raw") -> Path:
    """保存上传文件到 data/images/{assessment_id}/{kind}.jpg。"""
    folder = settings.data_dir / "images" / str(assessment_id)
    folder.mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename or "img.jpg").suffix or ".jpg"
    path = folder / f"{kind}{ext}"
    with path.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    return path


def rel_to_data(path: Path) -> str:
    """转成相对 data 目录的路径（存库用）。"""
    try:
        return str(Path(path).resolve().relative_to(settings.data_dir.resolve()))
    except ValueError:
        return str(path)
