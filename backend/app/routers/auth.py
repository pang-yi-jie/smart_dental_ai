"""认证接口：微信登录、诊所登录、管理员登录。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import AdminLoginRequest, ClinicLoginRequest, WechatLoginRequest
from app.services import auth_service

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/auth/wechat")
def wechat_login(req: WechatLoginRequest, db: Session = Depends(get_db)):
    try:
        return auth_service.wechat_login(db, req.phone, req.openid, req.code)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(400, str(exc))


@router.post("/clinic/login")
def clinic_login(req: ClinicLoginRequest, db: Session = Depends(get_db)):
    try:
        return auth_service.clinic_login(db, req.phone, req.password)
    except ValueError as exc:
        raise HTTPException(401, str(exc))


@router.post("/admin/login")
def admin_login(req: AdminLoginRequest):
    try:
        return auth_service.admin_login(req.username, req.password)
    except ValueError as exc:
        raise HTTPException(401, str(exc))
