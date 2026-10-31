"""认证相关请求模型。"""

from pydantic import BaseModel


class WechatLoginRequest(BaseModel):
    """家长微信登录。"""
    code: str | None = None
    phone: str
    openid: str | None = None


class PasswordLoginRequest(BaseModel):
    """学校/医生账号密码登录。"""
    phone: str
    password: str


class AdminLoginRequest(BaseModel):
    username: str
    password: str
