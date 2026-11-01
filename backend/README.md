# 家校医协同口腔健康管理小程序 —— 后端

FastAPI 后端。产品：儿童青少年口腔健康「家校医」协同管理（家长拍照筛查 → AI 风险分级 → 学校/医生协同）。

## 技术栈

- FastAPI + SQLAlchemy 2.x + SQLite（本地开发）/ PostgreSQL（生产）
- AI：YOLOv8 两段管线 —— ①牙位检测（OCC 咬合面 + Front 唇颊面）→ ②龋风险分类（待接入）
- 认证：JWT + bcrypt；角色：家长 / 学校（校医）/ 医生 / 平台管理员

## 目录结构

见 [后端代码导航.md](后端代码导航.md)（详细的文件/函数/接口对照表）。

## 运行

```bat
cd D:\SmartDentalAI\backend
D:\miniconda\envs\dental-ai\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

启动后：
- 健康检查：`GET http://127.0.0.1:8000/health`
- API 文档：`http://127.0.0.1:8000/docs`
- 首次启动自动建表 + 预加载 AI 模型

## 冒烟测试

```bat
D:\miniconda\envs\dental-ai\python.exe _smoke.py
```

跑通三端全流程：管理员建学校/校医/医生 → 家长登录建档 → 评估 → 医生确认。

## 测试账号

| 角色 | 账号 | 密码 |
|---|---|---|
| 家长 | 任意手机号（如 `13800138000`） | 无需密码 |
| 校医 | `13700000001` | `123456` |
| 医生 | `13600000001` | `123456` |
| 管理员 | `13455774393` | `Pang0328` |

> 校医/医生/管理员账号由 `_smoke.py` 创建；正式使用应通过管理员接口手动开通。

## 待办

1. **龋风险分类模型**（`services/ai_service.py` 的 `classify()` 是占位，返回 `risk_level=None`）
2. Celery + Redis 异步推理（当前同步）
3. 学校端 / 医生端小程序界面（后端接口已就绪）
