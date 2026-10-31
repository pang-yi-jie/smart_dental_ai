"""病例业务：创建病例 → AI 分析 → 写结果。"""

from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.models import AITask, Case, Diagnosis, Image
from app.services.ai_service import ai_service
from app.services.storage import rel_to_data, save_upload


def create_case_and_analyze(
    db: Session,
    user_id: int,
    view: str,
    file: UploadFile,
    tooth_position: str | None = None,
    clinic_id: int | None = None,
    owner_id: int | None = None,
) -> Case:
    """创建病例并同步跑 AI 分析，返回病例。

    MVP 采用同步推理（模型已预加载，单张 ~百毫秒）。
    并发上来后可改成 Celery 异步，逻辑不变。
    """
    case = Case(
        user_id=user_id,
        clinic_id=clinic_id,
        owner_id=owner_id,
        tooth_position=tooth_position,
        view=view,
        status="analyzing",
    )
    db.add(case)
    db.commit()
    db.refresh(case)

    # 存原始图
    raw = save_upload(file, case.id, "raw")
    db.add(Image(case_id=case.id, type="raw", path=rel_to_data(raw)))

    task = AITask(case_id=case.id, model=view, status="running")
    db.add(task)
    db.commit()

    try:
        result = ai_service.predict(raw, view)
        annotated = ai_service.annotate(raw, view, settings.data_dir / "images" / str(case.id))
        result["annotated_image"] = rel_to_data(annotated)
        db.add(Image(case_id=case.id, type="annotated", path=rel_to_data(annotated)))
        db.add(Diagnosis(case_id=case.id, ai_result=result))
        case.status = "pending"
        task.status = "done"
    except Exception as exc:  # noqa: BLE001
        case.status = "failed"
        task.status = "failed"
        task.error = str(exc)

    db.commit()
    db.refresh(case)
    return case
