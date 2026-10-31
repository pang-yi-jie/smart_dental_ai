"""家庭域：账户（家庭）+ 家庭成员。"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from app.database import Base


class Account(Base):
    """家庭账户：手机号唯一，地址挂在账户级。"""

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(32), unique=True, index=True, nullable=False)  # 手机号（应用层加密）
    address = Column(String(256), nullable=True)  # 地址（账户级）
    openid = Column(String(64), unique=True, index=True, nullable=True)  # 微信 openid
    created_at = Column(DateTime, server_default=func.now())


class FamilyMember(Base):
    """家庭成员：父亲/母亲/孩子N/自己。"""

    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    role = Column(String(16), nullable=False)        # father / mother / child / self
    name = Column(String(64), nullable=False)
    birth = Column(String(16), nullable=True)        # 出生年月
    gender = Column(String(8), nullable=True)        # male / female
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
