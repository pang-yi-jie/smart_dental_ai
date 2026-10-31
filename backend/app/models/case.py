"""病例相关：cases / images / diagnoses / reports / review_logs / ai_tasks。"""

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, func

from app.database import Base


class Case(Base):
    """一次检测记录。"""

    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)   # 患者
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=True, index=True)  # 空=个人自测
    owner_id = Column(Integer, ForeignKey("clinic_users.id"), nullable=True, index=True)  # 自己名下（操作员）
    tooth_position = Column(String(16), nullable=True)   # FDI 牙位，如 16
    view = Column(String(16), nullable=False)            # occlusal / buccal
    status = Column(String(16), default="uploaded", index=True)  # uploaded/analyzing/pending/finalized/rejected/failed
    created_at = Column(DateTime, server_default=func.now())


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    type = Column(String(16), nullable=False)   # raw / annotated
    path = Column(String(256), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Diagnosis(Base):
    """AI 原始 / 医生修改 / 最终，三份分存。"""

    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    ai_result = Column(JSON, nullable=True)
    doctor_edited = Column(JSON, nullable=True)
    final = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    content = Column(JSON, nullable=True)
    status = Column(String(16), default="draft")
    created_at = Column(DateTime, server_default=func.now())


class ReviewLog(Base):
    """医生修改留痕（审计）。"""

    __tablename__ = "review_logs"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    clinic_user_id = Column(Integer, ForeignKey("clinic_users.id"), nullable=False)
    changes = Column(JSON, nullable=False)
    reviewed_at = Column(DateTime, server_default=func.now())


class AITask(Base):
    __tablename__ = "ai_tasks"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    model = Column(String(16), nullable=False)          # occ / front
    status = Column(String(16), default="queued")       # queued/running/done/failed
    error = Column(String(256), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
