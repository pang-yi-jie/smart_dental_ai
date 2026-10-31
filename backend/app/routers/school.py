"""学校端（校医）接口：本校学生、代拍照、复核反馈、追踪进度。"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import require_role
from app.core.security import mask_phone
from app.database import get_db
from app.models import Account, Assessment, FamilyMember, Feedback, Result, Task
from app.services import assessment_service, family_service

router = APIRouter(prefix="/api/school", tags=["school"])


def _student_out(db: Session, m: FamilyMember) -> dict:
    acct = db.query(Account).get(m.account_id)
    return {
        "id": m.id, "name": m.name, "role": m.role,
        "birth": m.birth, "gender": m.gender,
        "phone": mask_phone(acct.phone) if acct else None,
    }


@router.get("/students")
def list_students(db: Session = Depends(get_db), payload: dict = Depends(require_role("school"))):
    school_id = payload.get("school_id")
    members = db.query(FamilyMember).filter(FamilyMember.school_id == school_id).all()
    return [_student_out(db, m) for m in members]


@router.get("/students/{member_id}/progress")
def student_progress(member_id: int, db: Session = Depends(get_db),
                     payload: dict = Depends(require_role("school"))):
    school_id = payload.get("school_id")
    m = db.query(FamilyMember).filter(FamilyMember.id == member_id, FamilyMember.school_id == school_id).first()
    if not m:
        raise HTTPException(404, "学生不存在或不在本校")
    tasks = db.query(Task).filter(Task.member_id == member_id).all()
    feedbacks = db.query(Feedback).join(Task).filter(Task.member_id == member_id).all()
    assessments = db.query(Assessment).filter(Assessment.member_id == member_id).all()
    return {
        "member": _student_out(db, m),
        "tasks": [{"id": t.id, "type": t.type, "status": t.status, "next_step": t.next_step} for t in tasks],
        "feedbacks": [{"id": f.id, "type": f.type, "content": f.content} for f in feedbacks],
        "assessment_count": len(assessments),
    }


@router.post("/assessments")
def create_assessment(
    member_id: int = Form(...),
    view: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(require_role("school")),
):
    """校医代拍照。"""
    school_id = payload.get("school_id")
    m = db.query(FamilyMember).filter(FamilyMember.id == member_id, FamilyMember.school_id == school_id).first()
    if not m:
        raise HTTPException(404, "学生不存在或不在本校")
    if view not in ("occlusal", "buccal"):
        raise HTTPException(400, "view 必须是 occlusal 或 buccal")
    q = family_service.get_questionnaire(db, member_id)
    questionnaire = q.answers if q else None
    a = assessment_service.create_assessment_and_analyze(db, member_id, view, file, questionnaire)
    return {"id": a.id, "member_id": a.member_id, "status": a.status, "risk_level": a.risk_level}


@router.post("/feedbacks/{feedback_id}/review")
def review_feedback(feedback_id: int, result: str = Form(...),
                    db: Session = Depends(get_db), payload: dict = Depends(require_role("school"))):
    """复核家长反馈。"""
    fb = db.query(Feedback).get(feedback_id)
    if not fb:
        raise HTTPException(404, "反馈不存在")
    task = db.query(Task).get(fb.task_id)
    if task:
        task.status = "done" if result == "resolved" else "pending"
        task.next_step = result
        db.commit()
    return {"ok": True}
