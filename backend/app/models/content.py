"""内容域：科普视频 + 商品（定向推送）。"""

from sqlalchemy import Column, DateTime, Integer, String, func

from app.database import Base


class Video(Base):
    """科普视频。"""

    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    url = Column(String(256), nullable=True)
    category = Column(String(32), index=True, nullable=True)
    status = Column(String(8), default="on")  # on / off
    created_at = Column(DateTime, server_default=func.now())


class Product(Base):
    """商品（好物推荐，淘口令带货）。"""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(32), index=True, nullable=False)
    title = Column(String(128), nullable=False)
    cover_image = Column(String(256), nullable=True)
    price = Column(String(32), nullable=True)
    description = Column(String(512), nullable=True)
    taobao_code = Column(String(128), nullable=True)
    taobao_url = Column(String(256), nullable=True)
    qr_image = Column(String(256), nullable=True)
    status = Column(String(8), default="on")
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
