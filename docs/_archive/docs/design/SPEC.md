# AgentHub 规范文档

> 版本: v2.0 | 创建时间: 2026-04-26 | 更新: 2026-04-26

## 概述

AgentHub 是一个**AI 工具管理平台**，旨在为多个 AI 工具提供中央化的配置管理、部署工具、网关接入和多端交互支持。

## 项目愿景

**让 AI 工具管理变得简单**

- 一键部署各种 AI 工具
- 中央化配置管理
- 统一网关接入（微信、QQ、飞书等）
- 多端交互支持（Web、TUI、CLI、GUI）

## 设计原则

| 原则 | 说明 |
|------|------|
| **工具无关** | 纯文本 Markdown，任何 AI 都能直接读取 |
| **中央化管理** | 所有配置集中在 `profiles/`、`skills/`、`agents/` |
| **单一真相** | 每类信息只存一处，不重复不冗余 |
| **可扩展** | 支持插件式接入新工具和新网关 |
| **多端支持** | 支持 Web、TUI、CLI、GUI 多种交互方式 |

## 核心模块

### 1. 工具管理 (Tool Management)

统一管理多种 AI 工具的配置：

| 工具 | 配置文件位置 | 说明 |
|------|-------------|------|
| OpenCode | `~/.config/opencode/` | AI 编程助手 |
| OpenClaw | `~/.openclaw/` | Agent 框架 |
| CodeBuddy | `~/.codebuddy/` | 代码助手 |
| Claude Desktop | `~/.claude/` | 对话助手 |
| Cursor | `~/.cursor/` | AI 编辑器 |
| Hermes | `~/.hermes/` | 终端助手 |

### 2. 部署中心 (Deployment Center)

- **Shell 脚本**: Linux/macOS/WSL
- **PowerShell**: Windows 原生
- **Docker**: 容器化部署

### 3. 网关接入 (Gateway Integration)

| 网关 | 协议 | 状态 |
|------|------|------|
| 微信 | WeChat API | 🔜 计划中 |
| QQ | OICQ/CQHTTP | 🔜 计划中 |
| 飞书 | Feishu API | 🔜 计划中 |
| Telegram | Bot API | 🔜 计划中 |
| Discord | Bot API | 🔜 计划中 |

### 4. 资源中心 (Resource Center)

| 资源 | 说明 |
|------|------|
| Skill 库 | 共享技能，可被多个工具引用 |
| Agent 库 | Agent 角色配置 |
| 提示词库 | 常用提示词模板 |

### 5. 多端交互 (Multi-Interface)

| 界面 | 技术栈 | 说明 |
|------|--------|------|
| Web | React/Vue | 浏览器访问 |
| TUI | Rich/Textual | 终端 UI |
| CLI | Python/Go | 命令行工具 |
| GUI | Tauri/Electron | 桌面应用 |

## 目录结构

```
agenthub/
├── SKILL.md                    # Skill 核心定义
├── README.md                   # 项目总览
├── SPEC.md                     # 本规范文档
├── LICENSE                     # MIT License
├── .gitignore
├── requirements.txt            # Python 依赖
├── pyproject.toml              # 项目配置
│
├── src/                        # 📦 源代码
│   ├── cli/                    # 💻 命令行入口
│   │   ├── main.py            # CLI 主入口
│   │   ├── utils.py           # 工具函数
│   │   └── commands/          # 子命令
│   │       ├── skill.py       # Skill 管理
│   │       ├── agent.py       # Agent 调度
│   │       ├── memory.py      # 记忆管理
│   │       ├── doc.py         # 文档生成
│   │       └── init.py        # 初始化
│   │
│   ├── core/                  # ⚙️ 核心模块
│   │   ├── skill/            # 🎯 Skill 管理
│   │   │   ├── registry.py   # Skill 注册表
│   │   │   ├── loader.py     # Skill 加载器
│   │   │   ├── sync.py       # Skill 同步
│   │   │   ├── version.py    # 版本管理
│   │   │   └── dependency.py # 依赖解析
│   │   │
│   │   ├── agent/            # 🤖 Agent 调度
│   │   │   ├── router.py     # 路由引擎
│   │   │   ├── scheduler.py  # 任务调度器
│   │   │   ├── state.py      # 状态管理
│   │   │   └── adapters/     # 适配器层
│   │   │       ├── base.py   # Adapter 基类
│   │   │       ├── claude.py # Claude Code
│   │   │       ├── codex.py  # Codex
│   │   │       ├── opencode.py # OpenCode
│   │   │       └── openclaw.py # OpenClaw
│   │   │
│   │   ├── memory/           # 🧠 多级记忆
│   │   │   ├── levels.py     # 记忆分级引擎 (L0-L4)
│   │   │   ├── short_term.py # 短期记忆
│   │   │   ├── long_term.py  # 长期记忆
│   │   │   ├── knowledge.py  # 知识图谱
│   │   │   ├── context.py    # 上下文提取
│   │   │   └── retrieval.py  # 记忆检索
│   │   │
│   │   ├── doc/             # 📝 文档生成
│   │   │   ├── generator.py  # 文档生成器
│   │   │   ├── readme.py     # README 生成
│   │   │   ├── changelog.py  # CHANGELOG 生成
│   │   │   ├── parser.py     # 代码文档解析
│   │   │   └── templates/   # 文档模板
│   │   │       ├── api.md
│   │   │       ├── skill.md
│   │   │       └── project.md
│   │   │
│   │   ├── mcp/             # 🔌 MCP 协议
│   │   │   ├── server.py     # MCP 服务器
│   │   │   ├── client.py    # MCP 客户端
│   │   │   └── tools.py     # MCP 工具管理
│   │   │
│   │   └── storage/          # 💾 存储层
│   │       ├── file_store.py   # 文件存储
│   │       ├── sqlite_store.py # SQLite 存储
│   │       ├── vector_store.py # 向量存储
│   │       └── migrate.py    # 数据迁移
│   │
│   └── config/               # ⚙️ 配置
│       ├── loader.py         # 配置加载器
│       └── default.yaml     # 默认配置
│
├── runtime/                   # 📁 运行时目录 (~/.agenthub/)
│   └── .gitkeep             # 不提交 Git
│
├── docs/                     # 📚 文档指南
│   ├── structure.md          # 目录结构
│   ├── quick-start.md       # 快速开始
│   ├── cli-design.md        # CLI 设计
│   ├── web-design.md        # Web 设计
│   ├── memory-design.md     # 多级记忆设计
│   ├── skill-format.md      # Skill 格式规范
│   ├── agent-protocol.md    # Agent 通信协议
│   └── supported-tools.md   # 支持的工具
│
├── scripts/                  # 🚀 工具脚本
│   ├── init.sh              # Linux/macOS 初始化
│   ├── init.ps1             # Windows 初始化
│   ├── gen-readme.py        # README 生成
│   ├── gen-changelog.py     # CHANGELOG 生成
│   └── setup-env.sh         # 环境安装
│
├── tests/                    # 🧪 测试
│   ├── test_skill.py
│   ├── test_agent.py
│   ├── test_memory.py
│   ├── test_doc.py
│   └── fixtures/            # 测试用例
│       └── sample-skill/
│
└── examples/                 # 📖 示例
    ├── skills/              # Skill 示例
    │   └── hello-world/
    └── agents/              # Agent 配置示例
        └── simple-router.yaml
```

### 用户数据目录 (~/.agenthub/)

```
~/.agenthub/                  # 用户本地数据（不在 Git 中）
├── memory/                   # 🧠 记忆系统
│   ├── short-term/          # 短期记忆 (TTL=24h)
│   │   └── {session_id}/
│   ├── long-term/           # 长期记忆
│   │   └── {entity}/
│   └── knowledge/            # 知识库
│
├── profile/                  # 👤 用户画像
│   ├── identity.md          # 身份信息
│   ├── skills.md           # 技能图谱
│   ├── projects.md         # 项目经验
│   ├── health/             # 健康记录
│   ├── growth/             # 成长轨迹
│   └── contacts/           # 联系人
│
├── skills/                   # 🛠️ 已安装的 Skill
├── agents/                   # 🤖 Agent 配置
├── config.yaml              # 全局配置
└── state.json               # 运行时状态
```

## 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 顶级目录 | 中文（skills/agents 除外） | `profile/`、`projects/` |
| skills/agents | 英文 | `skills/`、`agents/` |
| 技能目录 | 英文 kebab-case | `adb-wireless-debug` |
| 子目录/文件 | 中文 | `身份信息.md` |
| 联系人 | 中文 | `冯雪薇`、`黄海潼` |

## CLI 命令设计

```bash
as --help

AgentHub - AI 工具管理平台

用法:
  as <command> [options]

命令:
  init          初始化项目
  list          列出已安装工具
  install       安装 AI 工具
  config        配置管理
  skill         Skill 管理
  gateway       网关管理
  deploy        一键部署
  sync          同步配置

选项:
  -h, --help    显示帮助
  -v, --version 显示版本
```

## API 设计 (Web界面)

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/tools` | GET | 获取工具列表 |
| `/api/tools/:id` | GET | 获取工具详情 |
| `/api/tools/:id/start` | POST | 启动工具 |
| `/api/tools/:id/stop` | POST | 停止工具 |
| `/api/skills` | GET | 获取 Skill 列表 |
| `/api/gateways` | GET | 获取网关列表 |
| `/api/deploy` | POST | 部署工具 |

## 未来规划

### Phase 1 - 基础框架
- [ ] 项目结构设计
- [ ] 多工具配置文件解析器
- [ ] Skill 库中央管理

### Phase 2 - 部署系统
- [ ] AI 工具检测与安装
- [ ] 一键部署脚本
- [ ] 容器化支持

### Phase 3 - 网关接入
- [ ] 微信网关接入
- [ ] QQ 网关接入
- [ ] 飞书网关接入

### Phase 4 - 多端交互
- [ ] Web 管理界面
- [ ] TUI 终端界面
- [ ] CLI 命令行工具
- [ ] GUI 桌面应用

---

*创建：AgentHub - 2026-04-26*
