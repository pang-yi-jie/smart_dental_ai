"""统一导出所有 ORM 模型，确保 Base.metadata 能建全表。"""

from app.models.case import AITask, Case, Diagnosis, Image, Report, ReviewLog
from app.models.clinic import Clinic, ClinicUser
from app.models.product import Product
from app.models.user import User

__all__ = [
    "User",
    "Clinic",
    "ClinicUser",
    "Case",
    "Image",
    "Diagnosis",
    "Report",
    "ReviewLog",
    "AITask",
    "Product",
]
