# AgentHub · AI 使用指南

> **版本**: v1.0 | **适用**: 所有接入 AgentHub 的 AI 工具
>
> 本文件是 AI 接入 AgentHub 的核心规范，告知如何正确使用项目中的各个功能模块。

---

## 1. 项目概述

AgentHub 是一个**跨平台 AI 工具共享架构**，核心目标是：

- **统一 Skill 格式** — 一次编写，跨 AI 工具复用
- **统一 Agent 配置** — 一次配置，跨 AI 工具运行
- **统一记忆系统** — 跨 AI 工具持久化
- **统一用户画像** — 切换工具不丢失

```
                  ┌──────────────────┐
                  │  共享数据架构    │
                  │  ~/.agenthub/    │
                  └──────────────────┘
                    │    │    │    │
        ┌───────────┼────┼────┼────┼───────────┐
        ▼           ▼    ▼    ▼    ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ AI工具1  │ │ AI工具2  │ │ AI工具3  │ │ AI工具4  │
    └─────────┘ └─────────┘ └─────────┘ └─────────┘
        │           │           │           │
        ▼           ▼           ▼           ▼
    Skills/     Skills/     Skills/     Skills/
    Memory      Memory      Memory      Memory
    Profile     Profile     Profile     Profile
```

**核心价值**: 一次配置，处处运行；一次记忆，持续有效。

---

## 2. 共享数据架构（AgentHub）

> AgentHub 是一个跨 AI 工具的共享数据架构，为接入的 AI 工具提供共享资源
>
> **核心定位**：共享技能库 · 共享 Agent 库 · 共享用户画像 · 共享记忆系统
>
> **共享含义**：所有接入的 AI 工具都可以访问和使用 AgentHub 提供的共享资源

### 共享数据根目录
- `~/.agenthub/` — AgentHub 共享资源库

### 共享资源类型
| 资源 | 路径 | 说明 |
|------|------|------|
| 共享 Skill 库 | `~/.agenthub/skills/` | 所有 AI 工具可复用 |
| 共享 Agent 库 | `~/.agenthub/agents/` | 可复用的 Agent 模板 |
| 共享用户画像 | `~/.agenthub/profile/` | 跨工具统一用户画像 |
| 共享记忆系统 | `~/.agenthub/memory/` | 跨会话持久化记忆 |
| AI 工具注册表 | `memory/core/ai-registry.json` | 已接入的 AI 工具清单 |

### AI 工具注册表
- 路径：`memory/core/ai-registry.json`
- 说明：各 AI 工具在此注册，接入 AgentHub 共享架构

### 注册表结构
```json
{
  "tools": {
    "tool-name": {
      "name": "显示名称",
      "config_path": "配置目录路径",
      "skills_path": "技能库路径（可选）",
      "capabilities": {
        "subagents": ["子Agent列表"],
        "memory_system": true,
        "skills": true,
        "gateway": true,
        "channels": ["支持的通道"]
      },
      "last_updated": "最后更新时间"
    }
  }
}
```

### 工作流程
当收到"更新共享数据"指令时：
1. 遍历所有数据源文件夹
2. 对比 `~/.agenthub/` 中已存在的内容
3. 将没有的内容复制到对应共享目录

---

## 3. 目录结构

```
~/.agenthub/
├── AGENTS.md              ← AI 使用指南（你正在阅读）
├── README.md              ← 人类可读的项目介绍
│
├── skills/                # 🛠️ 技能库
│   ├── 00-SKILL-SPEC.md  # ★ Skill 编写规范
│   ├── {skill}/          # 每个 Skill 一个目录
│   │   └── SKILL.md      # Skill 定义文件
│   └── registry.json      # 已安装 Skill 索引
│
├── agents/                # 🤖 Agent 配置
│   ├── registry.json      # Agent 注册表
│   ├── router.md          # 路由规则
│   ├── main-agent.md      # 主 Agent 配置
│   └── {type}-agent.md    # 各专业 Agent 配置
│
├── memory/                # 🧠 记忆系统
│   ├── core/               #   核心记忆
│   │   ├── MEMORY.md      #   重要事实（用 § 分隔）
│   │   ├── USER.md        #   用户画像简要
│   │   └── ai-registry.json  # AI工具注册表
│   ├── hot/               #   短期记忆（会话级）
│   ├── cold/              #   中期记忆（7-30天）
│   ├── archive/           #   归档记忆（永久）
│   ├── SKILL.md           #   记忆系统 Skill
│   └── _index/            #   索引
│
├── profile/               # 👤 用户画像
│   ├── identity.yaml      #   身份信息
│   ├── skills.md          #   技能图谱
│   └── contacts/           #   联系人目录
│
├── TODO/                  # 📋 任务追踪
│   ├── 00-TODO-SPEC.md    #   TODO 规范
│   ├── README.md          #   使用说明
│   ├── 待办/              #   待开始任务
│   ├── 进行中/            #   进行中任务
│   └── 归档/              #   已完成任务
│
├── secrets/               # 🔐 敏感信息（不提交 Git）
└── docs/                  # 📚 设计文档（归档）
```

---

## 4. 核心模块详解

### 4.1 Skills（技能）

**用途**: 让 AI 掌握特定任务的执行方法，跨工具复用。

**Skill 文件格式**:
```yaml
---
name: skill-name
description: 简短描述
version: "1.0.0"
triggers: ["触发词1", "触发词2"]
---

# Skill 标题

## 触发条件
- 触发词：xxx

## 执行步骤
1. xxx
2. xxx

## 注意事项
- xxx
```

**AI 使用规范**:
- 当用户请求涉及某 Skill 领域时，先 `skill_view(name)` 加载完整内容
- 严格按照 Skill 中的步骤执行，不要跳过
- 发现 Skill 有错误，用 `skill_manage(action='patch')` 修复
- 复杂任务先创建 TODO 追踪进度

---

### 4.2 Agents（路由）

**用途**: 根据用户意图路由到最合适的专业 Agent 或 Skill。

**Agent 注册表** (`agents/registry.json`):
```json
{
  "agents": {
    "dev-agent": {
      "id": "dev-agent",
      "display_name": "开发专家",
      "capabilities": ["代码", "API", "网站"],
      "status": "active"
    }
  }
}
```

**路由规则** (`agents/router.md`):
| 关键词 | 路由目标 |
|--------|----------|
| 开发/代码/网站/API | dev-agent |
| 日程/课程/作业/天气/待办 | life-agent |
| 博客/邮件/飞书/文档/PPT | ops-agent |
| 自动化/脚本/批量 | productivity-agent |

**AI 使用规范**:
- 优先判断用户意图，路由到专业 Agent 或加载对应 Skill
- 无法判断时，使用通用处理流程
- 路由后确保传递完整上下文

---

### 4.3 Memory（记忆）

**用途**: 持久化 AI 与用户的交互历史，实现跨会话记忆。

**文件架构**:
```
memory/core/              ← 核心记忆（永久，AI 必读）
├── MEMORY.md            #   重要事实，分隔符 §
└── USER.md              #   用户画像简要
```

**MEMORY.md 格式**:
```markdown
# MEMORY.md

- 重要事实/偏好1
§
- 重要事实/偏好2
§
- 踩坑记录：xxx
```

**USER.md 格式**:
```markdown
# USER.md

## 基本信息
- 姓名：xxx
- 偏好：xxx
```

**AI 使用规范**:

| 时机 | 操作 |
|------|------|
| **对话开始** | 读取 `memory/core/MEMORY.md` + `USER.md` |
| **发现新信息** | 立即追加到 `memory/core/MEMORY.md`，用 `§` 分隔 |
| **用户纠正偏好** | 写入 `memory/core/USER.md` |
| **遇到错误/踩坑** | 追加到 `memory/core/MEMORY.md` |

**重要规则**:
- ❌ 不要覆盖 MEMORY.md 中的已有内容，只做追加
- ✅ 用 `§` 作为分隔符，独占一行
- ✅ AI 输出必须带署名：`[agent-id]`
- ✅ 定期整理：hot → cold → archive 的沉淀

---

### 4.4 Profile（用户画像）

**用途**: 存储用户的身份、偏好、联系人，让 AI 快速了解用户。

**文件结构**:
```
profile/
├── identity.yaml    # 基础信息（姓名/学校/职业等）
└── skills.md        # 技能清单（可选）
```

**identity.yaml 格式**:
```yaml
name: 用户姓名
email: example@mail.com
role: 开发工程师
preferences:
  - 喜欢结构清晰的文件夹分类
  - 用 Markdown 格式记录
```

**AI 使用规范**:
- 对话开始时读取 `profile/identity.yaml` 了解用户基础信息
- 用户纠正偏好时，更新对应文件

---

### 4.5 TODO（任务追踪）

**用途**: 追踪复杂任务的多步骤进度，确保不遗漏。

**文件命名**:
```
{序号}-{标题}.md
```
文件存放在对应状态目录中：`待办/` `进行中/` `归档/`

**状态流转**:
```
待办/ ──开始──▶ 进行中/ ──完成──▶ 归档/
  │                    │
  └──取消───────────────┴──────▶ 归档/
```

**文件格式**:
```yaml
---
id: "001"
title: "科目一学习计划"
status: "in_progress"
priority: "high"
created_by: "[agent-id]"
created_at: "2026-04-20T10:00:00Z"
updated_at: "2026-04-28T15:30:00Z"
due: "2026-08-01"
---

# 001 - 科目一学习计划

## 任务描述
暑假前通过科目一考试，每天刷题100道。

## 子任务
- [x] 刷完题库第一章
- [ ] 模拟考试达到90分以上
```

**AI 使用规范**:
| 场景 | 是否创建 TODO |
|------|---------------|
| 用户明确安排的任务 | ✅ |
| AI 自己承诺的里程碑 | ✅ |
| 多步骤复杂任务 | ✅ |
| 一次性简单任务 | ❌ |
| 用户说不用记录 | ❌ |

---

## 5. 模块联动

### 4.1 典型工作流

```
用户: "帮我开发一个博客网站"

1. [路由] 判断为开发任务，加载 dev-agent 或 web-development Skill
2. [记忆] 检查 memory/core/MEMORY.md 是否有关于博客的过往经验
3. [画像] 读取 profile/identity.yaml 了解用户技术栈
4. [技能] 加载 web-development SKILL
5. [TODO] 创建 `待办/001-博客开发.md` 追踪进度
6. [执行] 按 SKILL 步骤执行
7. [记忆] 完成/踩坑 → 追加到 `memory/core/MEMORY.md`
8. [归档] 任务完成 → TODO 移至 `归档/`
```

### 4.2 跨模块依赖

```
用户输入
    │
    ├── Skill ──▶ 加载执行方法
    ├── Agent ──▶ 路由到专业处理
    ├── Memory ─▶ 读取历史记忆（memory/core/MEMORY.md）
    ├── Profile ─▶ 读取用户画像（profile/）
    └── TODO ──▶ 记录/追踪进度
```

---

## 6. AI 初始化流程

接入 AgentHub 时，AI 应按以下顺序初始化：

```
Step 1: 读取本文件 (AGENTS.md)
    │
    ├── 读取 README.md 了解项目愿景
    ├── 读取 agents/registry.json 检查是否已注册
    ├── 读取 memory/core/ai-registry.json 了解已注册的 AI 工具
    └── 若未注册 → 执行注册流程
    │
Step 2: 加载核心记忆
    │
    ├── 读取 memory/core/MEMORY.md
    └── 读取 memory/core/USER.md
    │
Step 3: 加载用户画像
    │
    └── 读取 profile/identity.yaml
    │
Step 4: 检查待办
    │
    └── 读取 TODO/ 了解当前任务
    │
Step 5: 确认 Skill 库
    │
    └── 读取 skills/00-SKILL-SPEC.md 了解可用技能
```

---

## 7. 默认工作文件夹

**推荐设置**：将 AI 的默认工作文件夹设置为 `~/.agenthub/`

### 6.1 为什么推荐

| 优势 | 说明 |
|------|------|
| 配置集中 | Skill、Agent、记忆、画像都在同一目录 |
| 启动即读取 | AI 启动时自动加载配置，无需手动指定 |
| 跨工具共享 | 通过符号链接，多个 AI 工具共享同一配置 |

### 6.2 设置方法

**OpenCode**：在配置中设置默认工作目录
```json
{
  "working_directory": "~/.agenthub"
}
```

**Cursor**：打开 `~/.agenthub` 作为工作区

**其他工具**：将启动目录设置为 `~/.agenthub/`

### 6.3 工作模式

```
默认启动 → ~/.agenthub（读取配置、记忆、画像）
    │
    ├── 用户说"切换到 ~/projects/my-app"
    │   └── AI 切换到项目目录，开始开发
    │
    └── 用户说"回到 agenthub"
        └── AI 切换回 ~/.agenthub
```

**说明**：
- 配置/记忆始终在 `~/.agenthub`，不受工作目录影响
- 用户可随时切换到其他项目目录进行开发
- 切换后，AI 仍可读取 `~/.agenthub` 下的配置

---

## 8. 命名与格式规范

| 模块 | 格式要求 |
|------|----------|
| Skill 名 | 英文 kebab-case，如 `web-development` |
| Agent ID | 英文 kebab-case，如 `dev-agent` |
| 目录名 | 英文 kebab-case 或中文均可 |
| TODO 状态 | 目录名 `待办` `进行中` `归档` |
| 记忆分隔 | `§` 独占一行 |
| 时间格式 | ISO 8601，如 `2026-04-29T10:00:00Z` |
| AI 署名 | `[agent-id]` 格式 |

---

## 9. 禁止事项

- ❌ 不要在 `secrets/` 外的任何地方存储密钥
- ❌ 不要覆盖 `memories/MEMORY.md` 中的已有内容，只做追加
- ❌ 不要删除 `archive/` 中的归档记忆
- ❌ 不要出现任何私人路径或信息（保持开源通用）
- ❌ 不要使用 `TODO/` 文件夹追踪任务（这是用户专用的模板目录）

---

## 10. 快速索引

| 需要 | 路径 |
|------|------|
| 了解项目 | `./README.md` |
| 接入规范 | `./AGENTS.md` |
| 路由规则 | `./agents/router.md` |
| Skill 规范 | `./skills/00-SKILL-SPEC.md` |
| TODO 规范 | `./TODO/00-TODO-SPEC.md` |
| 记忆系统 | `./memory/core/MEMORY.md` |
| 设计文档 | `./docs/` |

---

*AgentHub · 愿景驱动，代码落地。*
*AI 接入规范 v2.0 · 2026-05-15*
