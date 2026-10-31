"""安全工具：密码哈希、JWT、手机号脱敏。"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import settings


def hash_password(password: str) -> str:
    """加密密码（bcrypt）。"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """校验密码。"""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def create_token(subject: str, role: str, extra: dict | None = None) -> str:
    """签发 JWT。subject=唯一标识(用户id/手机号)，role=patient/clinic/admin。"""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.token_expire_minutes),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    """解析 JWT，失败抛异常。"""
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])


def mask_phone(phone: str) -> str:
    """手机号脱敏：138****1234。"""
    if not phone or len(phone) < 7:
        return phone
    return f"{phone[:3]}****{phone[-4:]}"
