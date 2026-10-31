"""医生端（诊所后台）病例接口：只处理自己名下病例。"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import require_role
from app.core.security import mask_phone
from app.database import get_db
from app.models import Case, ClinicUser, Diagnosis, ReviewLog, User
from app.schemas.case import DiagnosisUpdate
from app.services import case_service

router = APIRouter(prefix="/api/clinic", tags=["clinic"])


def _me(db: Session, payload: dict) -> ClinicUser:
    cu = db.query(ClinicUser).get(int(payload["sub"]))
    if not cu:
        raise HTTPException(401, "账号不存在")
    return cu


@router.post("/cases")
def create_case(
    phone: str = Form(...),
    view: str = Form(...),
    tooth_position: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(require_role("clinic")),
):
    """诊所代测：医生用诊所相机拍，收患者手机号，建病例并分析。"""
    if view not in ("occlusal", "buccal"):
        raise HTTPException(400, "view 必须是 occlusal 或 buccal")
    me = _me(db, payload)
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        user = User(phone=phone)
        db.add(user)
        db.commit()
        db.refresh(user)
    case = case_service.create_case_and_analyze(
        db, user.id, view, file, tooth_position, me.clinic_id, me.id
    )
    return _case_detail(db, case)


def _case_detail(db: Session, case: Case) -> dict:
    diag = db.query(Diagnosis).filter(Diagnosis.case_id == case.id).first()
    user = db.query(User).get(case.user_id)
    return {
        "id": case.id,
        "patient_phone": mask_phone(user.phone) if user else None,
        "tooth_position": case.tooth_position,
        "view": case.view,
        "status": case.status,
        "created_at": case.created_at.isoformat() if case.created_at else None,
        "ai_result": diag.ai_result if diag else None,
        "doctor_edited": diag.doctor_edited if diag else None,
        "final": diag.final if diag else None,
    }


@router.get("/cases")
def list_cases(status: str | None = None, db: Session = Depends(get_db),
               payload: dict = Depends(require_role("clinic"))):
    me = _me(db, payload)
    q = db.query(Case).filter(Case.owner_id == me.id)
    if status:
        q = q.filter(Case.status == status)
    return [_case_detail(db, c) for c in q.order_by(Case.id.desc()).all()]


@router.get("/cases/{case_id}")
def get_case(case_id: int, db: Session = Depends(get_db),
             payload: dict = Depends(require_role("clinic"))):
    me = _me(db, payload)
    case = db.query(Case).filter(Case.id == case_id, Case.owner_id == me.id).first()
    if not case:
        raise HTTPException(404, "病例不存在")
    return _case_detail(db, case)


@router.put("/cases/{case_id}/diagnosis")
def update_diagnosis(case_id: int, req: DiagnosisUpdate, db: Session = Depends(get_db),
                     payload: dict = Depends(require_role("clinic"))):
    me = _me(db, payload)
    case = db.query(Case).filter(Case.id == case_id, Case.owner_id == me.id).first()
    if not case:
        raise HTTPException(404, "病例不存在")
    diag = db.query(Diagnosis).filter(Diagnosis.case_id == case.id).first()
    if not diag:
        diag = Diagnosis(case_id=case.id)
        db.add(diag)
    diag.doctor_edited = req.diagnosis
    db.add(ReviewLog(case_id=case.id, clinic_user_id=me.id, changes=req.diagnosis))
    db.commit()
    return {"ok": True}


@router.post("/cases/{case_id}/finalize")
def finalize(case_id: int, db: Session = Depends(get_db),
             payload: dict = Depends(require_role("clinic"))):
    me = _me(db, payload)
    case = db.query(Case).filter(Case.id == case_id, Case.owner_id == me.id).first()
    if not case:
        raise HTTPException(404, "病例不存在")
    diag = db.query(Diagnosis).filter(Diagnosis.case_id == case.id).first()
    final = (diag.doctor_edited if diag and diag.doctor_edited
             else (diag.ai_result if diag else None))
    if diag:
        diag.final = final
    case.status = "finalized"
    db.commit()
    return {"ok": True, "final": final}


@router.post("/cases/{case_id}/reject")
def reject(case_id: int, db: Session = Depends(get_db),
           payload: dict = Depends(require_role("clinic"))):
    me = _me(db, payload)
    case = db.query(Case).filter(Case.id == case_id, Case.owner_id == me.id).first()
    if not case:
        raise HTTPException(404, "病例不存在")
    case.status = "rejected"
    db.commit()
    return {"ok": True}
