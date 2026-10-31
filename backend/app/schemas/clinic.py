"""诊所相关请求模型。"""

from pydantic import BaseModel


class ClinicUserCreate(BaseModel):
    """管理员创建医生账号。"""
    clinic_id: int
    name: str
    phone: str
    password: str
