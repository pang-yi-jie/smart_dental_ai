"""家庭业务：成员管理 + 档案级问卷。"""

from sqlalchemy.orm import Session

from app.models import FamilyMember, Questionnaire


def list_members(db: Session, account_id: int):
    return db.query(FamilyMember).filter(FamilyMember.account_id == account_id).all()


def get_member(db: Session, account_id: int, member_id: int):
    return (
        db.query(FamilyMember)
        .filter(FamilyMember.id == member_id, FamilyMember.account_id == account_id)
        .first()
    )


def create_member(db: Session, account_id: int, role: str, name: str,
                  birth: str | None = None, gender: str | None = None,
                  school_id: int | None = None):
    m = FamilyMember(
        account_id=account_id, role=role, name=name,
        birth=birth, gender=gender, school_id=school_id,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


def save_questionnaire(db: Session, member_id: int, answers: dict):
    q = db.query(Questionnaire).filter(Questionnaire.member_id == member_id).first()
    if not q:
        q = Questionnaire(member_id=member_id, answers=answers)
        db.add(q)
    else:
        q.answers = answers
    db.commit()
    return q


def get_questionnaire(db: Session, member_id: int):
    return db.query(Questionnaire).filter(Questionnaire.member_id == member_id).first()
