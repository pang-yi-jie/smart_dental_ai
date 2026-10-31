"""数据库连接与 ORM 基类。

SQLAlchemy 2.x；本地 SQLite，上线换 PostgreSQL 只改 config.database_url。
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

connect_args = {}
if settings.database_url.startswith("sqlite"):
    # SQLite 需要允许跨线程（FastAPI 多线程）
    connect_args["check_same_thread"] = False

engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def get_db():
    """FastAPI 依赖：每个请求一个数据库会话，用完自动关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
