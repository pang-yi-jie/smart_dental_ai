"""平台管理端接口：学校/校医/医生/视频/商品 管理。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import require_role
from app.core.security import hash_password
from app.database import get_db
from app.models import Doctor, Product, School, SchoolUser, Video
from app.schemas.product import ProductCreate

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Depends(require_role("admin"))],
)


# ---------- 学校 ----------

@router.get("/schools")
def list_schools(db: Session = Depends(get_db)):
    return [{"id": s.id, "name": s.name, "status": s.status} for s in db.query(School).all()]


@router.post("/schools")
def create_school(name: str, db: Session = Depends(get_db)):
    s = School(name=name)
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"id": s.id, "name": s.name, "status": s.status}


# ---------- 校医账号 ----------

@router.post("/school-users")
def create_school_user(school_id: int, name: str, phone: str, password: str,
                       db: Session = Depends(get_db)):
    u = SchoolUser(school_id=school_id, name=name, phone=phone, password_hash=hash_password(password))
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"id": u.id, "school_id": u.school_id, "name": u.name, "phone": u.phone}


@router.get("/school-users")
def list_school_users(db: Session = Depends(get_db)):
    return [{"id": u.id, "school_id": u.school_id, "name": u.name, "phone": u.phone}
            for u in db.query(SchoolUser).all()]


# ---------- 医生账号 ----------

@router.post("/doctors")
def create_doctor(name: str, phone: str, password: str, db: Session = Depends(get_db)):
    d = Doctor(name=name, phone=phone, password_hash=hash_password(password))
    db.add(d)
    db.commit()
    db.refresh(d)
    return {"id": d.id, "name": d.name, "phone": d.phone}


@router.get("/doctors")
def list_doctors(db: Session = Depends(get_db)):
    return [{"id": d.id, "name": d.name, "phone": d.phone} for d in db.query(Doctor).all()]


# ---------- 科普视频 ----------

@router.post("/videos")
def create_video(title: str, url: str = "", category: str = "", db: Session = Depends(get_db)):
    v = Video(title=title, url=url, category=category)
    db.add(v)
    db.commit()
    db.refresh(v)
    return {"id": v.id, "title": v.title}


@router.delete("/videos/{vid}")
def delete_video(vid: int, db: Session = Depends(get_db)):
    v = db.query(Video).get(vid)
    if not v:
        raise HTTPException(404, "视频不存在")
    v.status = "off"
    db.commit()
    return {"ok": True}


# ---------- 商品 ----------

@router.post("/products")
def create_product(req: ProductCreate, db: Session = Depends(get_db)):
    p = Product(**req.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "title": p.title}


@router.put("/products/{pid}")
def update_product(pid: int, req: ProductCreate, db: Session = Depends(get_db)):
    p = db.query(Product).get(pid)
    if not p:
        raise HTTPException(404, "商品不存在")
    for k, v in req.model_dump().items():
        setattr(p, k, v)
    db.commit()
    return {"ok": True}


@router.delete("/products/{pid}")
def delete_product(pid: int, db: Session = Depends(get_db)):
    p = db.query(Product).get(pid)
    if not p:
        raise HTTPException(404, "商品不存在")
    p.status = "off"
    db.commit()
    return {"ok": True}
