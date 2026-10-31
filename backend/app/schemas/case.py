"""病例相关请求模型。"""

from pydantic import BaseModel


class CaseCreate(BaseModel):
    view: str                       # occlusal / buccal
    tooth_position: str | None = None
    clinic_id: int | None = None    # 诊所代测时传入
    owner_id: int | None = None     # 操作员（自己名下）


class DiagnosisUpdate(BaseModel):
    diagnosis: dict                 # 医生修改后的结构化结果
    suggestion: str | None = None
