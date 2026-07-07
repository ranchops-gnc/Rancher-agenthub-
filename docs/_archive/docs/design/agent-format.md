# Agent 格式规范 v1.0

> 版本: v1.0 | 更新: 2026-04-27

## 概述

Agent 是 AgentHub 的核心调度单元，每个 Agent 是一个专业角色，可处理特定类型的任务并调用相关 Skills。

## 目录结构

```
agent-name/                  # Agent 根目录（英文 kebab-case）
├── AGENT.md                 # ★ 核心定义（必需）
├── README.md                # 使用文档（可选）
├── prompts/                 # Prompt 模板
│   ├── system.md           # 系统提示词
│   └── user.md             # 用户交互模板
├── skills/                  # 绑定的 Skill（软链接或配置）
│   └── skill-name.yaml     # Skill 配置
├── memory/                  # 记忆配置
│   └── memory.yaml
└── references/              # 参考资料
    └── *.md
```

## AGENT.md 格式

```yaml
---
name: agent-name             # Agent 名称（英文 kebab-case）
version: 1.0.0             # SemVer 格式
type: specialist|router     # 类型：专家型 | 路由型
description: 简短描述       # 一句话说明
author: 作者名               # 作者

# 路由配置（type: router 时必需）
router:
  keywords:                 # 路由关键词
    - "关键词1"
    - "关键词2"
  priority: 10              # 优先级（数字越大越优先）
  fallback: other-agent      # 备选 Agent

# 专业配置（type: specialist 时必需）
specialist:
  domain:                   # 专业领域
    - "领域1"
    - "领域2"
  capabilities:             # 能力列表
    - "能力1"
    - "能力2"

# 技能绑定
skills:
  - skill-name@^1.0.0      # 必需 Skill
  - optional-skill@*        # 可选 Skill

# 记忆配置
memory:
  short_term:
    max_items: 100          # 短期记忆最大条目
    ttl_minutes: 30         # 过期时间
  long_term:
    enabled: true           # 是否启用长期记忆
    embedding: true         # 是否向量化

# 适配的 AI 工具
platforms:
  - opencode
  - openclaw
  - claude
  - hermes

# 配置
config:
  timeout_seconds: 300      # 超时时间
  max_retries: 3            # 最大重试次数
  parallel_tasks: 2         # 并行任务数

license: MIT
homepage: https://...       # 主页（可选）
source: https://...         # 源码地址（可选）
---

# Agent 正文（Markdown）

这里是 Agent 的详细说明。

## 职责

描述 Agent 的主要职责。

## 工作流程

描述 Agent 处理任务的典型流程。

## 与其他 Agent 的协作

描述与其他 Agent 的协作方式。
```

## 字段说明

### 必需字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | Agent 名称，英文 kebab-case，唯一 |
| `version` | string | SemVer 格式，如 `1.0.0` |
| `type` | enum | 类型：specialist（专家型）或 router（路由型） |
| `description` | string | 一句话简短描述 |

### Router 类型必需字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `router.keywords` | string[] | 路由关键词数组 |
| `router.priority` | int | 优先级 |
| `router.fallback` | string | 备选 Agent 名称 |

### Specialist 类型必需字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `specialist.domain` | string[] | 专业领域 |
| `specialist.capabilities` | string[] | 能力列表 |

### 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `author` | string | 作者名 |
| `skills` | string[] | 绑定的 Skill（格式：`name@version`） |
| `memory` | object | 记忆配置 |
| `platforms` | string[] | 支持的平台 |
| `config` | object | 行为配置 |
| `license` | string | 许可证 |
| `homepage` | string | 主页 URL |
| `source` | string | 源码地址 |

## Agent 类型

### Router（路由型）

负责接收请求并分发到专业 Agent，类似总机调度。

```yaml
type: router
router:
  keywords:
    - "开发"
    - "代码"
    - "编程"
  priority: 10
  fallback: main-agent
```

### Specialist（专家型）

负责处理特定领域的任务，直接执行或调用 Skills。

```yaml
type: specialist
specialist:
  domain:
    - "全栈开发"
    - "API 设计"
  capabilities:
    - "前端开发"
    - "后端开发"
    - "数据库设计"
skills:
  - frontend-dev@^1.0.0
  - api-design@^1.0.0
```

## 记忆配置

### 短期记忆

```yaml
memory:
  short_term:
    max_items: 100
    ttl_minutes: 30
```

### 长期记忆

```yaml
memory:
  long_term:
    enabled: true
    embedding: true
    vector_store: chroma
    top_k: 5
```

## 版本管理

使用 [SemVer](https://semver.org/) 格式：

- `1.0.0` - 正式版
- `0.1.0` - 开发版
- `1.0.0-beta.1` - 测试版

## 依赖解析

### Skill 依赖

```yaml
skills:
  - github-pr@^1.0.0      # 必需
  - hello-world@*          # 可选（* 表示任意版本）
```

### 循环依赖处理

- **禁止**：Agent 不能依赖自己（直接循环）
- **检测**：加载时检测循环依赖并报错
- **解决**：重新设计依赖结构

## 安装流程

1. **解析**：读取 AGENT.md，提取元数据
2. **验证**：检查技能依赖是否满足
3. **加载**：复制到 `~/.agenthub/agents/`
4. **注册**：添加到本地注册表
5. **初始化**：加载 Skills，建立记忆索引

## 存储位置

```
~/.agenthub/                  # 用户本地数据
├── agents/                   # 已安装的 Agent
│   ├── dev-agent/
│   │   └── AGENT.md
│   ├── life-agent/
│   │   └── AGENT.md
│   └── router/
│       └── main-agent.md
├── agent_registry.json     # 本地注册表
└── skills/                  # 共享 Skills
```

## 注册表格式

```json
{
  "agents": {
    "dev-agent": {
      "name": "dev-agent",
      "version": "1.0.0",
      "type": "specialist",
      "path": "~/.agenthub/agents/dev-agent",
      "installed_at": "2026-04-27T10:00:00Z",
      "source": "local"
    }
  },
  "index_updated_at": "2026-04-27T10:00:00Z"
}
```

## 多工具兼容性

| 工具 | 支持度 | 说明 |
|------|--------|------|
| OpenCode | ✅ | 通过 `~/.config/opencode/agents/` |
| OpenClaw | ✅ | 通过 `~/.openclaw/agents/` |
| Claude Code | ✅ | 通过 `~/.claude/agents/` |
| Hermes | ✅ | 通过 `~/.hermes/agents/` |

## 示例

### 最小 Agent

```yaml
---
name: hello-agent
version: 1.0.0
type: specialist
description: Hello World 示例
specialist:
  domain: ["示例"]
  capabilities: ["打招呼"]
---

# Hello Agent

这是一个示例 Agent。

## 功能

- 打招呼
- 回答简单问题
```

### 完整 Agent

```yaml
---
name: dev-agent
version: 1.0.0
type: specialist
description: 开发任务专家 Agent
author: Xavier
specialist:
  domain:
    - "全栈开发"
    - "移动开发"
    - "API 设计"
  capabilities:
    - "前端开发"
    - "后端开发"
    - "Android 开发"
    - "小程序开发"
skills:
  - github@^1.0.0
  - git@^1.0.0
  - android-debug@^1.0.0
memory:
  short_term:
    max_items: 100
    ttl_minutes: 60
  long_term:
    enabled: true
platforms:
  - opencode
  - openclaw
  - hermes
config:
  timeout_seconds: 600
  max_retries: 3
license: MIT
---

# Dev Agent

开发任务专家 Agent，负责处理所有开发相关的任务。

## 职责

- 接收开发任务需求
- 分析技术栈和实现方案
- 调用相关 Skills 执行任务
- 返回开发结果

## 工作流程

1. 理解用户需求
2. 加载必要的 Skills
3. 执行开发任务
4. 返回结果和总结
```

### Router Agent

```yaml
---
name: main-agent
version: 1.0.0
type: router
description: 主路由 Agent
router:
  keywords:
    - "开发"
    - "代码"
    - "编程"
    - "网站"
    - "API"
    - "Android"
    - "日程"
    - "课程"
    - "作业"
    - "天气"
    - "情感"
    - "博客"
    - "飞书"
    - "微信"
    - "邮件"
    - "PPT"
    - "自动化"
    - "脚本"
  priority: 100
  fallback: productivity-agent
---

# Main Agent

主路由 Agent，负责接收所有请求并分发到专业 Agent。

## 路由规则

| 需求类型 | 路由到 |
|----------|--------|
| 开发任务 | dev-agent |
| 生活服务 | life-agent |
| 运营任务 | ops-agent |
| 效率工具 | productivity-agent |

## 约束

1. 不喧宾夺主
2. 传递完整上下文
3. 记录交接
4. 汇总结果
```

---

*本文档由 AgentHub 自动生成*
