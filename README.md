# 口腔 AI 检测系统（SmartDentalAI）

面向口腔医疗机构定制的 AI 辅助检测系统。

**核心流程**：患者拍照 → AI 自动识别牙位并标注 → 医生在线复核 → 生成检测报告。

## 系统组成

| 端 | 使用人 | 形态 | 目录 |
|---|---|---|---|
| 患者端 | 患者 | 微信小程序 | `miniprogram/` |
| 医生端 / 管理端 | 医生 / 平台管理员 | Web 后台 | `backend/static/` |
| 后端服务 | — | FastAPI | `backend/app/` |

## 技术栈

- 后端：FastAPI + SQLAlchemy + PostgreSQL（本地开发用 SQLite）
- AI：YOLOv8 检测（OCC 咬合面 + Front 唇颊面），PyTorch CUDA
- 前端：微信小程序（原生）+ 医生 Web 后台（原生 HTML/JS）
- 部署：阿里云 ECS + frp 内网穿透

## 目录结构

```
backend/            # 后端（FastAPI 应用）
miniprogram/        # 微信小程序
docs/               # 文档
```

## 文档

- [后端架构设计.md](后端架构设计.md) —— 系统架构与决策
- [backend/后端代码导航.md](backend/后端代码导航.md) —— 后端代码索引
- [开发环境说明.md](开发环境说明.md) —— 开发环境搭建
- [项目文档索引.md](项目文档索引.md) —— 文档总览

## 快速开始

见 [开发环境说明.md](开发环境说明.md) 和 [backend/README.md](backend/README.md)。
