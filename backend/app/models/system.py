"""系统域：审计日志 + AI 任务。"""

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, func

from app.database import Base


class ReviewLog(Base):
    """操作留痕（审计）。"""

    __tablename__ = "review_logs"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False, index=True)
    operator_id = Column(Integer, nullable=False)
    changes = Column(JSON, nullable=False)
    reviewed_at = Column(DateTime, server_default=func.now())


class AITask(Base):
    """AI 推理任务。"""

    __tablename__ = "ai_tasks"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False, index=True)
    model = Column(String(16), nullable=False)
    status = Column(String(16), default="queued")
    error = Column(String(256), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
