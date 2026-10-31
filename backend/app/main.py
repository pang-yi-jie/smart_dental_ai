"""FastAPI 入口：装配路由、启动时建表 + 预加载 AI 模型。

启动（在 backend 目录下）:
    uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app import models  # noqa: F401  确保所有 ORM 模型注册到 Base
from app.config import settings
from app.database import Base, engine
from app.routers import admin, auth, cases, clinic, health, products
from app.services.ai_service import ai_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 建表（MVP；上线改用 Alembic 迁移）
    Base.metadata.create_all(bind=engine)
    # 预加载检测模型进显存，避免首个请求卡顿
    ai_service.preload()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

settings.data_dir.mkdir(parents=True, exist_ok=True)
# 静态文件：标注图等，访问路径 /files/...
app.mount("/files", StaticFiles(directory=str(settings.data_dir)), name="files")

# 医生后台网页（静态文件）
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/web", StaticFiles(directory=str(STATIC_DIR), html=True), name="web")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/web/login.html")


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(cases.router)
app.include_router(clinic.router)
app.include_router(products.router)
app.include_router(admin.router)
