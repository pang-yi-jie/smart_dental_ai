"""医生端接口：看所有人评估、确认诊断报告。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import require_role
from app.database import get_db
from app.models import Assessment, FamilyMember, Result

router = APIRouter(prefix="/api/doctor", tags=["doctor"])


@router.get("/assessments")
def list_assessments(db: Session = Depends(get_db), payload: dict = Depends(require_role("doctor"))):
    """医生看所有人的评估。"""
    items = db.query(Assessment).order_by(Assessment.id.desc()).all()
    out = []
    for a in items:
        result = db.query(Result).filter(Result.assessment_id == a.id).first()
        member = db.query(FamilyMember).get(a.member_id)
        out.append({
            "id": a.id, "member_id": a.member_id,
            "member_name": member.name if member else None,
            "status": a.status, "risk_level": a.risk_level,
            "detections": result.detections if result else None,
            "classification": result.classification if result else None,
            "doctor_confirmed": result.doctor_confirmed if result else False,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        })
    return out


@router.post("/assessments/{assessment_id}/confirm")
def confirm(assessment_id: int, db: Session = Depends(get_db),
            payload: dict = Depends(require_role("doctor"))):
    """医生确认诊断报告。"""
    result = db.query(Result).filter(Result.assessment_id == assessment_id).first()
    if not result:
        raise HTTPException(404, "结果不存在")
    result.doctor_confirmed = True
    result.confirmed_by = int(payload["sub"])
    db.commit()
    return {"ok": True}
