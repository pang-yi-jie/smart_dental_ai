"""用户表：个人（全局身份 = 手机号）。"""

from sqlalchemy import Column, DateTime, Integer, String, func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(32), unique=True, index=True, nullable=False)  # 手机号（应用层加密）
    openid = Column(String(64), unique=True, index=True, nullable=True)  # 微信 openid
    created_at = Column(DateTime, server_default=func.now())
