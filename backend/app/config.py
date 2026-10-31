"""全局配置。

所有可配置项集中在这里，用环境变量 `DENTAL_*` 或 `.env` 覆盖。
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DENTAL_", env_file=".env")

    # 应用
    app_name: str = "SmartDentalAI Backend"

    # 数据库：本地开发用 SQLite，上线切 PostgreSQL 只需改这一行
    # 例：postgresql+psycopg://user:pass@host:5432/dental
    database_url: str = f"sqlite:///{(BASE_DIR / 'data' / 'app.db').as_posix()}"

    # 文件存储目录
    data_dir: Path = BASE_DIR / "data"

    # JWT
    jwt_secret: str = "dev-secret-change-me-in-production"
    jwt_algorithm: str = "HS256"
    token_expire_minutes: int = 60 * 24

    # AI 推理
    inference_conf: float = 0.25
    inference_imgsz: int = 384

    # 平台管理员（MVP 用配置账号，后续可换 admins 表；上线建议改 .env 覆盖）
    admin_username: str = "13455774393"
    admin_password: str = "Pang0328"


settings = Settings()
