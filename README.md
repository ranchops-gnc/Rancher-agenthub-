# AgentHub

> 统一 AI 工具的 Skill · Agent · 用户画像 · 记忆系统 四大共享生态

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 这是什么？

AgentHub 是一个**跨平台 AI 工具管理平台**，解决以下问题：

| 问题 | 解决方案 |
|------|----------|
| 多个 AI 工具配置散落各处 | 中央化配置管理 |
| 每换工具都要重新配置 | 一键部署脚本 |
| AI 工具之间无法协作 | 统一网关接入 |
| Skill 库难以共享和复用 | 中央 Skill 资源库 |

---

## ✨ 四大核心模块

### 1️⃣ Skill 库 — 一次编写，到处运行

| 特性 | 说明 |
|------|------|
| **统一格式** | YAML frontmatter + Markdown，工具无关 |
| **跨平台兼容** | OpenClaw / OpenCode / Claude Code 通用 |
| **依赖管理** | SemVer 版本控制，自动解析依赖 |
| **触发词机制** | 智能匹配用户输入，自动加载 Skill |

```
skills/
├── github-pr/              # GitHub PR 管理
├── browser-bridge/         # 浏览器自动化
└── 50+ 共享 Skill
```

### 2️⃣ Agent 系统 — 专业角色，智能路由

| 特性 | 说明 |
|------|------|
| **类型定义** | Router（路由型）+ Specialist（专家型） |
| **技能绑定** | 自动加载所需 Skills |
| **记忆配置** | 短期/长期记忆策略可定制 |

```
agents/
├── main-agent/             # 主路由入口
├── dev-agent/              # 开发专家
├── life-agent/             # 生活服务
└── productivity-agent/     # 效率工具
```

### 3️⃣ 用户画像 — 工具无关，永久携带

| 特性 | 说明 |
|------|------|
| **统一格式** | YAML + Markdown，纯文本工具无关 |
| **身份信息** | 基础资料、联系方式、社交账号 |
| **偏好设置** | 审美偏好、沟通风格、回复习惯 |

```
profile/
├── identity.yaml           # 身份信息
├── skills.md              # 技能图谱
└── contacts/              # 联系人
```

### 4️⃣ 记忆系统 — 持久记忆，持续学习

| 特性 | 说明 |
|------|------|
| **简化设计** | core + session + persist 三级（参考 Hermes） |
| **核心记忆** | MEMORY.md + USER.md，永久保留 |
| **会话记忆** | 运行时内存，定期归档 |

```
memory/
├── core/                   # 核心记忆（永久）
│   ├── MEMORY.md          #   重要事实（用 § 分隔）
│   └── USER.md            #   用户画像
├── session/                # 会话记忆（运行时）
└── persist/                # 持久化记忆（归档）
```

---

## 🚀 快速安装

### 一键安装（推荐）

```bash
curl -fsSL https://raw.githubusercontent.com/xuanyuanluoxue/AgentHub/main/misc/install.sh -o /tmp/install.sh && bash /tmp/install.sh
```

运行后显示菜单，选择操作：

| 选项 | 说明 |
|------|------|
| `1` | 安装 AgentHub |
| `2` | 更新 AgentHub |
| `3` | 重新安装 |
| `4` | 卸载 AgentHub |
| `5` | 打开配置目录 |
| `6` | 退出 |

### 安装位置

```
~/.agenthub/   # Linux/macOS/WSL
```

安装后运行 `agenthub --help` 查看帮助。

---

## 🤖 AI 接入指南

将以下内容复制给 AI 阅读：

```
请先阅读 ~/.agenthub/AGENTS.md 了解 AgentHub 接入规范。
```

或者让 AI 执行以下步骤：

1. 读取 `~/.agenthub/AGENTS.md` — AI 使用指南
2. 读取 `~/.agenthub/agents/registry.json` — 检查是否已注册
3. 读取 `~/.agenthub/memory/core/MEMORY.md` — 加载核心记忆
4. 读取 `~/.agenthub/profile/identity.yaml` — 了解用户

---

## 📁 目录结构

```
~/.agenthub/
├── AGENTS.md              # ★ AI 使用指南
├── README.md              # 本文件
│
├── skills/                # Skill 库
│   ├── 00-SKILL-SPEC.md  #   Skill 编写规范
│   └── {skill}/          #   各 Skill 目录
│
├── agents/                # Agent 配置
│   ├── registry.json      #   Agent 注册表
│   ├── router.md          #   路由规则
│   └── {type}-agent.md   #   各 Agent 配置
│
├── memory/                # 记忆系统
│   ├── core/              #   核心记忆
│   ├── session/          #   会话记忆
│   └── persist/          #   持久化记忆
│
├── profile/               # 用户画像
│   ├── identity.yaml      #   身份信息
│   └── contacts/          #   联系人
│
├── TODO/                  # 任务追踪
│   ├── 00-TODO-SPEC.md   #   TODO 规范
│   └── README.md          #   使用说明
│
├── secrets/               # 敏感信息（不提交 Git）
└── docs/                  # 设计文档
```

---

## 📚 文档导航

| 文档 | 说明 |
|------|------|
| [AGENTS.md](./AGENTS.md) | **★ AI 必读** — AI 使用指南核心 |
| [skills/00-SKILL-SPEC.md](./skills/00-SKILL-SPEC.md) | Skill 编写规范 |
| [memory/SKILL.md](./memory/SKILL.md) | 记忆系统说明 |
| [TODO/00-TODO-SPEC.md](./TODO/00-TODO-SPEC.md) | TODO 任务追踪规范 |

---

## ⚠️ 隐私声明

> AgentHub 是**公共开源模板项目**，不包含任何私人信息。
>
> - 所有文档中的路径、账号、人名等均为**占位符**
> - 如需使用，请基于模板创建你自己的配置

---

## 📄 License

MIT License

---

*愿景驱动，代码落地。*
