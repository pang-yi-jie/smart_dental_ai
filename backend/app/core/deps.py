"""FastAPI 依赖注入：鉴权相关。"""

from fastapi import Depends, Header, HTTPException

from app.core.security import decode_token


def get_token_payload(authorization: str = Header(default=None)) -> dict:
    """从 Authorization: Bearer <token> 解析出 payload，未登录/过期抛 401。"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登录")
    token = authorization[len("Bearer "):]
    try:
        return decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")


def require_role(*roles: str):
    """生成「只允许指定角色访问」的依赖。

    用法：
        @router.get(...)
        def f(payload: dict = Depends(require_role("clinic", "admin"))): ...
    """
    def _dep(payload: dict = Depends(get_token_payload)) -> dict:
        if payload.get("role") not in roles:
            raise HTTPException(status_code=403, detail="无权限")
        return payload
    return _dep
