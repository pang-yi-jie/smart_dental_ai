"""认证相关请求/响应模型。"""

from pydantic import BaseModel


class WechatLoginRequest(BaseModel):
    """微信登录。生产环境用 code 换 openid/手机号；MVP 直接传 phone。"""
    code: str | None = None
    phone: str
    openid: str | None = None


class ClinicLoginRequest(BaseModel):
    phone: str
    password: str


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
