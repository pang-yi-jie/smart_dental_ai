"""认证业务：家长 / 学校 / 医生 / 管理员登录。"""

from sqlalchemy.orm import Session

from app.config import settings
from app.core.security import create_token, verify_password
from app.models import Account, Doctor, SchoolUser


def family_login(db: Session, phone: str, openid: str | None = None, code: str | None = None) -> dict:
    """家长登录：手机号 → 家庭账户。"""
    acct = db.query(Account).filter(Account.phone == phone).first()
    if not acct:
        acct = Account(phone=phone, openid=openid)
        db.add(acct)
        db.commit()
        db.refresh(acct)
    elif openid and not acct.openid:
        acct.openid = openid
        db.commit()

    token = create_token(str(acct.id), "family")
    return {"access_token": token, "role": "family", "account_id": acct.id}


def school_login(db: Session, phone: str, password: str) -> dict:
    """校医登录。"""
    user = db.query(SchoolUser).filter(SchoolUser.phone == phone).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("账号或密码错误")
    token = create_token(str(user.id), "school", extra={"school_id": user.school_id})
    return {
        "access_token": token,
        "role": "school",
        "school_id": user.school_id,
        "user_id": user.id,
        "name": user.name,
    }


def doctor_login(db: Session, phone: str, password: str) -> dict:
    """医生登录（看所有人，只确认诊断）。"""
    user = db.query(Doctor).filter(Doctor.phone == phone).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("账号或密码错误")
    token = create_token(str(user.id), "doctor")
    return {"access_token": token, "role": "doctor", "user_id": user.id, "name": user.name}


def admin_login(username: str, password: str) -> dict:
    """平台管理员登录（配置账号）。"""
    if username != settings.admin_username or password != settings.admin_password:
        raise ValueError("管理员账号或密码错误")
    token = create_token(settings.admin_username, "admin")
    return {"access_token": token, "role": "admin"}
