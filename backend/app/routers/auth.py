"""认证接口：家长 / 学校 / 医生 / 管理员登录。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import AdminLoginRequest, PasswordLoginRequest, WechatLoginRequest
from app.services import auth_service

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/auth/wechat")
def family_login(req: WechatLoginRequest, db: Session = Depends(get_db)):
    try:
        return auth_service.family_login(db, req.phone, req.openid, req.code)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(400, str(exc))


@router.post("/school/login")
def school_login(req: PasswordLoginRequest, db: Session = Depends(get_db)):
    try:
        return auth_service.school_login(db, req.phone, req.password)
    except ValueError as exc:
        raise HTTPException(401, str(exc))


@router.post("/doctor/login")
def doctor_login(req: PasswordLoginRequest, db: Session = Depends(get_db)):
    try:
        return auth_service.doctor_login(db, req.phone, req.password)
    except ValueError as exc:
        raise HTTPException(401, str(exc))


@router.post("/admin/login")
def admin_login(req: AdminLoginRequest):
    try:
        return auth_service.admin_login(req.username, req.password)
    except ValueError as exc:
        raise HTTPException(401, str(exc))
