"""患者端病例接口。"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import require_role
from app.database import get_db
from app.models import Case, Diagnosis
from app.services import case_service

router = APIRouter(prefix="/api", tags=["cases"])


def _case_out(db: Session, case: Case) -> dict:
    diag = db.query(Diagnosis).filter(Diagnosis.case_id == case.id).first()
    return {
        "id": case.id,
        "tooth_position": case.tooth_position,
        "view": case.view,
        "status": case.status,
        "created_at": case.created_at.isoformat() if case.created_at else None,
        "ai_result": diag.ai_result if diag else None,
        "doctor_edited": diag.doctor_edited if diag else None,
        "final": diag.final if diag else None,
    }


@router.post("/cases")
def create_case(
    view: str = Form(...),
    tooth_position: str = Form(""),
    clinic_id: int | None = Form(None),
    owner_id: int | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(require_role("patient")),
):
    if view not in ("occlusal", "buccal"):
        raise HTTPException(400, "view 必须是 occlusal 或 buccal")
    case = case_service.create_case_and_analyze(
        db, int(payload["sub"]), view, file, tooth_position, clinic_id, owner_id
    )
    return _case_out(db, case)


@router.get("/cases/{case_id}")
def get_case(case_id: int, db: Session = Depends(get_db),
             payload: dict = Depends(require_role("patient"))):
    case = db.query(Case).get(case_id)
    if not case or case.user_id != int(payload["sub"]):
        raise HTTPException(404, "病例不存在")
    return _case_out(db, case)


@router.get("/my/cases")
def my_cases(db: Session = Depends(get_db),
             payload: dict = Depends(require_role("patient"))):
    cases = (
        db.query(Case)
        .filter(Case.user_id == int(payload["sub"]))
        .order_by(Case.id.desc())
        .all()
    )
    return [_case_out(db, c) for c in cases]
