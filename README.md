# 家校医协同口腔健康管理小程序（SmartDentalAI）

面向儿童青少年的口腔健康「家校医」协同管理平台：**家长**拍照筛查 + AI 龋风险分级，**学校（校医）**跟踪督导，**医生**确认诊断。

## 核心流程

```
图片收集（上下颌）→ 健康问卷 → AI 分析（牙位检测→龋风险分级）→ 评估报告 → 干预建议 → 反馈闭环
```

## 系统组成

| 端 | 使用人 | 形态 | 目录 |
|---|---|---|---|
| 家长端 | 家长 | 微信小程序 | `miniprogram/` |
| 学校端 / 医生端 | 校医 / 医生 | 小程序（后续） | 后端接口已就绪 |
| 后端服务 | — | FastAPI | `backend/` |

## 技术栈

- 后端：FastAPI + SQLAlchemy + SQLite/PostgreSQL + JWT
- AI：YOLOv8 两段管线（①牙位检测 OCC/Front → ②龋风险分类），PyTorch CUDA
- 前端：原生微信小程序 + TDesign 组件库 + LESS
- 部署：阿里云 ECS + frp 内网穿透（电脑核心计算）

## 目录结构

```
backend/            # 后端（FastAPI 应用）
miniprogram/        # 微信小程序（家长端）
data/               # 数据库 + 图片（运行时生成，已 gitignore）
yolov8-segment/     # AI 模型训练产物（已 gitignore）
```

## 文档

| 文档 | 说明 |
|---|---|
| [后端架构设计.md](后端架构设计.md) | ⭐ 系统架构与所有决策（v7） |
| [miniprogram/前端代码导航.md](miniprogram/前端代码导航.md) | ⭐ 小程序前端代码索引 |
| [backend/后端代码导航.md](backend/后端代码导航.md) | 后端代码索引 |
| [开发环境说明.md](开发环境说明.md) | 开发环境搭建 |
| [项目文档索引.md](项目文档索引.md) | 文档总览 |

## 快速开始

1. 后端：见 [backend/README.md](backend/README.md)
2. 小程序：微信开发者工具打开 `miniprogram/`，勾选「不校验合法域名」
3. 详见 [开发环境说明.md](开发环境说明.md)
