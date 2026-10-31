# SmartDentalAI 后端

牙科 AI 检测后端（FastAPI）。当前已实现：AI 推理服务（OCC 咬合面 + Front 唇颊面牙位检测）。

## 目录结构

```
backend/
├── schema.sql              # PostgreSQL 建表脚本（9 张表）
├── app/
│   ├── __init__.py
│   ├── config.py           # 配置（数据库、数据目录）
│   ├── ai_service.py       # AI 推理服务（模型加载 + 路由 + 结构化结果）
│   └── main.py             # FastAPI 入口（/health /predict /annotate）
└── requirements.txt        # 依赖（见项目根 requirements.txt）
```

## 运行

```bat
cd D:\SmartDentalAI\backend
D:\miniconda\envs\dental-ai\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 接口

- `GET  /health` 健康检查
- `POST /predict` 上传图片 + view → 结构化 JSON（牙位检测结果）
- `POST /annotate` 上传图片 + view → 标注图

`view` 取值：`occlusal`（咬合面→OCC 模型）、`buccal`（唇颊面→Front 模型）。

## 自测 AI 服务

```bat
D:\miniconda\envs\dental-ai\python.exe -m app.ai_service "图片路径" occlusal
```

## 下一步（待实现）

1. 用户/诊所/病例/报告 的 ORM 模型 + 路由（按 schema.sql）
2. 微信登录（openid + 手机号授权）
3. Celery + Redis 异步任务（上传→推理→回写）
4. 阿里云 Nginx + frp 配置
