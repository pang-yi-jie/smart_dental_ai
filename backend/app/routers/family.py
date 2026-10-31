"""家长端接口：成员、评估、问卷、任务反馈。"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import require_role
from app.database import get_db
from app.models import Assessment, FamilyMember, Feedback, Image, Result, Task
from app.schemas.family import MemberCreate, QuestionnaireSubmit
from app.services import assessment_service, family_service

router = APIRouter(prefix="/api", tags=["family"])


def _member_out(m: FamilyMember) -> dict:
    return {
        "id": m.id, "role": m.role, "name": m.name,
        "birth": m.birth, "gender": m.gender, "school_id": m.school_id,
    }


def _assessment_out(db: Session, a: Assessment) -> dict:
    result = db.query(Result).filter(Result.assessment_id == a.id).first()
    annotated = db.query(Image).filter(Image.assessment_id == a.id, Image.type == "annotated").first()
    return {
        "id": a.id, "member_id": a.member_id, "status": a.status,
        "risk_level": a.risk_level,
        "created_at": a.created_at.isoformat() if a.created_at else None,
        "detections": result.detections if result else None,
        "classification": result.classification if result else None,
        "annotated_image": annotated.path if annotated else None,
    }


# ---------- 成员 ----------

@router.get("/members")
def list_members(db: Session = Depends(get_db), payload: dict = Depends(require_role("family"))):
    acct_id = int(payload["sub"])
    return [_member_out(m) for m in family_service.list_members(db, acct_id)]


@router.post("/members")
def create_member(req: MemberCreate, db: Session = Depends(get_db),
                  payload: dict = Depends(require_role("family"))):
    acct_id = int(payload["sub"])
    m = family_service.create_member(db, acct_id, req.role, req.name, req.birth, req.gender, req.school_id)
    return _member_out(m)


# ---------- 问卷（档案级） ----------

@router.post("/members/{member_id}/questionnaire")
def save_questionnaire(member_id: int, req: QuestionnaireSubmit,
                       db: Session = Depends(get_db), payload: dict = Depends(require_role("family"))):
    acct_id = int(payload["sub"])
    m = family_service.get_member(db, acct_id, member_id)
    if not m:
        raise HTTPException(404, "成员不存在")
    family_service.save_questionnaire(db, member_id, req.answers)
    return {"ok": True}


@router.get("/members/{member_id}/questionnaire")
def get_questionnaire(member_id: int, db: Session = Depends(get_db),
                      payload: dict = Depends(require_role("family"))):
    acct_id = int(payload["sub"])
    m = family_service.get_member(db, acct_id, member_id)
    if not m:
        raise HTTPException(404, "成员不存在")
    q = family_service.get_questionnaire(db, member_id)
    return {"answers": q.answers if q else None}


# ---------- 评估 ----------

@router.post("/assessments")
def create_assessment(
    member_id: int = Form(...),
    view: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(require_role("family")),
):
    acct_id = int(payload["sub"])
    m = family_service.get_member(db, acct_id, member_id)
    if not m:
        raise HTTPException(404, "成员不存在")
    if view not in ("occlusal", "buccal"):
        raise HTTPException(400, "view 必须是 occlusal 或 buccal")
    q = family_service.get_questionnaire(db, member_id)
    questionnaire = q.answers if q else None
    a = assessment_service.create_assessment_and_analyze(db, member_id, view, file, questionnaire)
    return _assessment_out(db, a)


@router.get("/members/{member_id}/assessments")
def member_assessments(member_id: int, db: Session = Depends(get_db),
                       payload: dict = Depends(require_role("family"))):
    acct_id = int(payload["sub"])
    m = family_service.get_member(db, acct_id, member_id)
    if not m:
        raise HTTPException(404, "成员不存在")
    items = db.query(Assessment).filter(Assessment.member_id == member_id).order_by(Assessment.id.desc()).all()
    return [_assessment_out(db, a) for a in items]


@router.get("/assessments/{assessment_id}")
def get_assessment(assessment_id: int, db: Session = Depends(get_db),
                   payload: dict = Depends(require_role("family"))):
    acct_id = int(payload["sub"])
    a = db.query(Assessment).get(assessment_id)
    if not a:
        raise HTTPException(404, "评估不存在")
    m = db.query(FamilyMember).get(a.member_id)
    if not m or m.account_id != acct_id:
        raise HTTPException(404, "无权访问")
    return _assessment_out(db, a)


# ---------- 任务 / 反馈 ----------

@router.get("/members/{member_id}/tasks")
def member_tasks(member_id: int, db: Session = Depends(get_db),
                 payload: dict = Depends(require_role("family"))):
    acct_id = int(payload["sub"])
    m = family_service.get_member(db, acct_id, member_id)
    if not m:
        raise HTTPException(404, "成员不存在")
    tasks = db.query(Task).filter(Task.member_id == member_id).order_by(Task.id.desc()).all()
    return [
        {"id": t.id, "type": t.type, "assignee": t.assignee, "status": t.status, "next_step": t.next_step}
        for t in tasks
    ]


@router.post("/tasks/{task_id}/feedback")
def submit_feedback(task_id: int, type: str = Form(...), content: str = Form(""),
                    db: Session = Depends(get_db), payload: dict = Depends(require_role("family"))):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(404, "任务不存在")
    acct_id = int(payload["sub"])
    m = db.query(FamilyMember).get(task.member_id)
    if not m or m.account_id != acct_id:
        raise HTTPException(404, "无权访问")
    fb = Feedback(task_id=task_id, type=type, content=content)
    db.add(fb)
    task.status = "feedback"
    db.commit()
    return {"ok": True}
