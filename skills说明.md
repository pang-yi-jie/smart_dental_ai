# 已安装的 Skill 库

> 安装位置：`C:\Users\<用户>\.dsh\skills\`
> 安装日期：2026-10-31
> 来源：https://pro.huxiu.com/article/4840706.html（实测 78 个 skills，这 5 个组合最香）

这套 skill 覆盖**产品开发全生命周期**：原型 → UI → 规划 → 开发 → 沉淀。

---

## 一、五个 Skill 一览

| 阶段 | Skill | 作用 |
|---|---|---|
| 原型阶段 | `brainstorming` | 把混乱的想法变成清晰的选择题，理清产品方向 |
| UI 阶段 | `ui-ux-pro-max` | 79 种样式、192 套配色、74 种字体组合，直接生成可落地的界面设计 |
| 规划阶段 | `planning-with-files` | Manus-style 规划，自动生成任务文件，进度一目了然 |
| 开发阶段 | `test-driven-development` | 先写测试再写代码，重构也能秒级验证 |
| 沉淀阶段 | `claudeception` | 基于项目对话生成专属 skills，把经验变成可复用的武器 |

---

## 二、各 Skill 详情

### 1. brainstorming（原型阶段）

- **来源**：https://github.com/obra/superpowers
- **文件**：8 个（75.7 KB）
- **何时用**：做任何新产品、新功能、新模块之前，先把「一堆想法」变成「清晰的选择题」
- **怎么触发**：「先帮我头脑风暴一下」「我不知道要做成什么样」
- **产出**：一系列选择题（产品定位、目标用户、功能范围、技术栈）→ 逐步收敛出产品形态
- **价值**：避免一上来就做「什么都有的大杂烩」，用选择题逼自己做决策

### 2. ui-ux-pro-max（UI 阶段）⭐ 最丰富

- **来源**：https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **文件**：73 个（3.5 MB，含本地可搜索数据库）
- **内置数据**：
  - 79 种可搜索样式（50 种活跃）
  - 192 套产品配色 + 推理配置
  - 74 种字体搭配
  - 119 条 UX 准则
  - 105 个图标
  - 17 个 GSAP 动效预设
  - 25 种图表类型
  - 22 个技术栈适配
- **何时用**：设计/重构任何界面（页面、组件、设计系统、响应式布局、配色、字体、图表）
- **关键技巧**（来自原文实测）：**要给足设计约束**，不能只说「设计好看点」。要把产品调性翻译成设计语言：
  > 例：这是一个游戏化的人生 RPG 小程序。核心交互是资源分配。设计风格要年轻、有游戏感但不幼稚。用色要清新，避免传统理财软件的严肃蓝绿色。参考 Monument Valley 的极简几何 + Duolingo 的激励感。

### 3. planning-with-files（规划阶段）

- **来源**：https://github.com/othmanadi/planning-with-files
- **文件**：33 个（486.5 KB）
- **核心机制**：在磁盘上维护三个文件
  - `task_plan.md` —— 任务计划
  - `findings.md` —— 调研发现
  - `progress.md` —— 进度记录
- **何时用**：多步骤、需要 5+ 次工具调用的复杂任务
- **价值**：
  - 随时问「我现在做到哪了」，能准确回答进度
  - 长任务不会忘记前面做了什么
  - 小项目不必用，**大项目必用**

### 4. test-driven-development（开发阶段）

- **来源**：https://github.com/obra/superpowers
- **文件**：2 个（17.4 KB）
- **何时用**：实现任何功能或修 bug 之前，**先写测试**
- **价值**：
  - 算法/逻辑类代码反复重构时，每次都能秒级验证
  - 小程序这类调试成本高的场景（改完要重新编译、真机扫码），测试是保命的
- **配套文件**：`writing-good-tests.md`

### 5. claudeception（沉淀阶段）

- **来源**：https://github.com/blader/Claudeception
- **文件**：6 个（36.5 KB）
- **何时用**：
  - 说「把这个存成 skill」「从这段对话里提炼一个 skill」
  - 说「我们学到了什么？」
  - 刚做完一次非平凡的调试 / 绕过某个坑 / 试错探索之后
- **价值**：把这次的踩坑经验和解决方案，固化成以后能直接复用的 skill

---

## 三、推荐工作流

```
想法混乱
   ↓  brainstorming（变成选择题）
产品方向清晰
   ↓  ui-ux-pro-max（生成高保真界面）
界面定了
   ↓  planning-with-files（拆任务、排里程碑）
任务清晰
   ↓  test-driven-development（先测试后编码）
代码跑通
   ↓  claudeception（提炼经验成可复用 skill）
越用越强
```

---

## 四、怎么调用

直接描述需求即可，DSH 会自动匹配。也可以明确指定：

- 「用 brainstorming 帮我想想做点什么」
- 「用 ui-ux-pro-max 重新设计小程序首页，参考 WeUI 规范」
- 「用 planning-with-files 规划一下这个项目的开发任务」
- 「用 test-driven-development 写这个算法」
- 「把这次调试经验用 claudeception 存成 skill」

---

## 五、注意事项

1. **不是越多越好**。原文作者装了 78 个，大部分从没用过。这 5 个是精挑的。
2. **小项目别用 planning-with-files**，大项目才值得。
3. **ui-ux-pro-max 必须给足约束**，否则出来的东西很平庸（原文作者踩过这个坑）。
4. **claudeception 的 scripts/resources 未完整下载**（GitHub API 限流），但核心 SKILL.md 完整可用，不影响使用。
