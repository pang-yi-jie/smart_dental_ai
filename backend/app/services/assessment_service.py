"""评估业务：建评估 → 存图 → AI 两段分析 → 写结果。"""

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.models import AITask, Assessment, Image, Result
from app.services.ai_service import ai_service
from app.services.storage import rel_to_data, save_upload


def create_assessment_and_analyze(
    db: Session,
    member_id: int,
    view: str,
    file: UploadFile,
    questionnaire=None,
) -> Assessment:
    """创建评估并同步跑 AI 两段分析。"""
    assessment = Assessment(member_id=member_id, status="analyzing")
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    raw = save_upload(file, assessment.id, "raw")
    db.add(Image(assessment_id=assessment.id, type=view, path=rel_to_data(raw)))

    task = AITask(assessment_id=assessment.id, model=view, status="running")
    db.add(task)
    db.commit()

    try:
        result = ai_service.analyze(raw, view, questionnaire)
        annotated = ai_service.annotate(raw, view, settings.data_dir / "images" / str(assessment.id))
        result["annotated_image"] = rel_to_data(annotated)
        db.add(Image(assessment_id=assessment.id, type="annotated", path=rel_to_data(annotated)))
        db.add(Result(
            assessment_id=assessment.id,
            detections=result["detections"],
            classification=result["classification"],
        ))
        assessment.status = "done"
        assessment.risk_level = result["risk_level"]
        task.status = "done"
    except Exception as exc:  # noqa: BLE001
        assessment.status = "failed"
        task.status = "failed"
        task.error = str(exc)

    db.commit()
    db.refresh(assessment)
    return assessment
