"""商品请求模型。"""

from pydantic import BaseModel


class ProductCreate(BaseModel):
    category: str
    title: str
    cover_image: str | None = None
    price: str | None = None
    description: str | None = None
    taobao_code: str | None = None
    taobao_url: str | None = None
    qr_image: str | None = None
    sort_order: int = 0
    status: str = "on"
