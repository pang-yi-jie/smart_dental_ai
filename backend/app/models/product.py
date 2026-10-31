"""商品表：好物推荐（淘口令带货）。"""

from sqlalchemy import Column, DateTime, Integer, String, func

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(32), index=True, nullable=False)  # device/toothpaste/toothbrush/other
    title = Column(String(128), nullable=False)
    cover_image = Column(String(256), nullable=True)
    price = Column(String(32), nullable=True)
    description = Column(String(512), nullable=True)
    taobao_code = Column(String(128), nullable=True)   # 淘口令
    taobao_url = Column(String(256), nullable=True)    # 淘宝链接（备用）
    qr_image = Column(String(256), nullable=True)      # 二维码（备用）
    status = Column(String(8), default="on")           # on / off
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
