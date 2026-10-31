"""诊所（租户）与诊所操作员。"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from app.database import Base


class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    status = Column(String(16), default="active")  # active / suspended
    created_at = Column(DateTime, server_default=func.now())


class ClinicUser(Base):
    __tablename__ = "clinic_users"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False, index=True)
    name = Column(String(64), nullable=False)
    phone = Column(String(32), nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
