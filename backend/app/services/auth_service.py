"""认证业务：微信登录、诊所登录、管理员登录。"""

from sqlalchemy.orm import Session

from app.config import settings
from app.core.security import create_token, verify_password
from app.models import ClinicUser, User


def wechat_login(db: Session, phone: str, openid: str | None = None, code: str | None = None) -> dict:
    """微信登录：手机号为主身份。

    生产环境：用 code 调微信 code2session + getPhoneNumber 拿真实手机号。
    MVP：直接用传入的 phone（前端授权后把手机号传过来）。
    """
    # TODO(生产)：接入微信 code2session / getPhoneNumber
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        user = User(phone=phone, openid=openid)
        db.add(user)
        db.commit()
        db.refresh(user)
    elif openid and not user.openid:
        user.openid = openid
        db.commit()

    token = create_token(str(user.id), "patient")
    return {"access_token": token, "role": "patient", "user_id": user.id}


def clinic_login(db: Session, phone: str, password: str) -> dict:
    """诊所操作员登录。"""
    user = db.query(ClinicUser).filter(ClinicUser.phone == phone).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("账号或密码错误")
    token = create_token(str(user.id), "clinic", extra={"clinic_id": user.clinic_id})
    return {
        "access_token": token,
        "role": "clinic",
        "clinic_id": user.clinic_id,
        "user_id": user.id,
        "name": user.name,
    }


def admin_login(username: str, password: str) -> dict:
    """平台管理员登录（MVP 用配置文件账号，后续可换成 admins 表）。"""
    if username != settings.admin_username or password != settings.admin_password:
        raise ValueError("管理员账号或密码错误")
    token = create_token(settings.admin_username, "admin")
    return {"access_token": token, "role": "admin"}
