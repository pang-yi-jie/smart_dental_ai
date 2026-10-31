"""健康评估域：评估记录 + 档案问卷 + 图片 + 分析结果 + 任务 + 反馈。"""

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, func

from app.database import Base


class Assessment(Base):
    """一次评估记录（图片收集 + 分析 + 报告）。"""

    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("family_members.id"), nullable=False, index=True)
    status = Column(String(16), default="uploaded", index=True)  # uploaded/analyzing/done/failed
    risk_level = Column(String(8), nullable=True)  # low / mid / high
    created_at = Column(DateTime, server_default=func.now())


class Questionnaire(Base):
    """档案级生活习惯问卷（填一次，偶尔更新）。"""

    __tablename__ = "questionnaires"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("family_members.id"), nullable=False, unique=True, index=True)
    answers = Column(JSON, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Image(Base):
    """图片：上颌/下颌/标注图/单牙裁图。"""

    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False, index=True)
    type = Column(String(16), nullable=False)  # upper / lower / annotated / crop
    path = Column(String(256), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Result(Base):
    """AI 分析结果 + 医生确认状态。"""

    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False, index=True)
    detections = Column(JSON, nullable=True)      # 牙位检测结果
    classification = Column(JSON, nullable=True)  # 龋风险分类结果
    doctor_confirmed = Column(Boolean, default=False)
    confirmed_by = Column(Integer, nullable=True)  # 医生 id
    created_at = Column(DateTime, server_default=func.now())


class Task(Base):
    """护牙计划任务：护理/学习/就诊。"""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("family_members.id"), nullable=False, index=True)
    type = Column(String(16), nullable=False)  # care / learn / visit
    assignee = Column(String(32), nullable=True)  # 责任方
    status = Column(String(16), default="pending")  # pending / done / feedback
    next_step = Column(String(256), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class Feedback(Base):
    """家长反馈：不会做 / 做不好 / 做不到。"""

    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False, index=True)
    type = Column(String(16), nullable=False)  # cannot / hard / fail
    content = Column(String(256), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
