"""平台管理端接口：诊所管理 + 商品增删改。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import require_role
from app.core.security import hash_password
from app.database import get_db
from app.models import Clinic, ClinicUser, Product
from app.schemas.clinic import ClinicUserCreate
from app.schemas.product import ProductCreate

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Depends(require_role("admin"))],
)


# ---------- 诊所 ----------

@router.get("/clinics")
def list_clinics(db: Session = Depends(get_db)):
    return [{"id": c.id, "name": c.name, "status": c.status}
            for c in db.query(Clinic).all()]


@router.post("/clinics")
def create_clinic(name: str, db: Session = Depends(get_db)):
    c = Clinic(name=name)
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "name": c.name, "status": c.status}


@router.post("/clinic-users")
def create_clinic_user(req: ClinicUserCreate, db: Session = Depends(get_db)):
    """创建医生账号（账号密码）。"""
    cu = ClinicUser(
        clinic_id=req.clinic_id,
        name=req.name,
        phone=req.phone,
        password_hash=hash_password(req.password),
    )
    db.add(cu)
    db.commit()
    db.refresh(cu)
    return {"id": cu.id, "clinic_id": cu.clinic_id, "name": cu.name, "phone": cu.phone}


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
