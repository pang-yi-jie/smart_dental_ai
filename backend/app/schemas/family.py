"""家庭相关请求模型。"""

from pydantic import BaseModel


class MemberCreate(BaseModel):
    role: str                       # father / mother / child / self
    name: str
    birth: str | None = None        # 出生年月
    gender: str | None = None       # male / female
    school_id: int | None = None


class QuestionnaireSubmit(BaseModel):
    answers: dict
