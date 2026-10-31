"""管理单位域：学校 + 校医账号 + 医生账号。"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from app.database import Base


class School(Base):
    """学校。"""

    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    status = Column(String(16), default="active")  # active / suspended
    created_at = Column(DateTime, server_default=func.now())


class SchoolUser(Base):
    """校医账号（学校端）。"""

    __tablename__ = "school_users"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    name = Column(String(64), nullable=False)
    phone = Column(String(32), nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Doctor(Base):
    """医生账号（看所有人，只确认诊断报告）。"""

    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    phone = Column(String(32), nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
