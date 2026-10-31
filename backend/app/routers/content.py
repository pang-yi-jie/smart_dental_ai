"""内容接口：科普视频 + 好物推荐。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product, Video

router = APIRouter(prefix="/api", tags=["content"])


# ---------- 科普视频 ----------

@router.get("/videos")
def list_videos(category: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Video).filter(Video.status == "on")
    if category:
        q = q.filter(Video.category == category)
    return [{"id": v.id, "title": v.title, "url": v.url, "category": v.category} for v in q.all()]


# ---------- 商品 ----------

def _ser(p: Product) -> dict:
    return {
        "id": p.id, "category": p.category, "title": p.title,
        "cover_image": p.cover_image, "price": p.price,
        "description": p.description, "taobao_code": p.taobao_code,
        "taobao_url": p.taobao_url, "qr_image": p.qr_image, "sort_order": p.sort_order,
    }


@router.get("/products")
def list_products(category: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Product).filter(Product.status == "on")
    if category:
        q = q.filter(Product.category == category)
    return [_ser(p) for p in q.order_by(Product.sort_order, Product.id).all()]


@router.get("/products/{pid}")
def get_product(pid: int, db: Session = Depends(get_db)):
    p = db.query(Product).get(pid)
    if not p or p.status != "on":
        raise HTTPException(404, "商品不存在或已下架")
    return _ser(p)
