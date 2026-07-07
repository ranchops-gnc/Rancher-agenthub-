# AgentHub - AI 工具管理平台

> 图形化管理和部署 AI 工具的中央控制中心

[![Stars](https://img.shields.io/github/stars/xuanyuanluoxue/AgentHub)](https://github.com/xuanyuanluoxue/AgentHub/stargazers)
[![License](https://img.shields.io/github/license/xuanyuanluoxue/AgentHub)](LICENSE)

## 🎯 这是什么？

AgentHub 是一个**AI 工具管理平台**，解决以下问题：

| 问题 | 解决方案 |
|------|----------|
| 多个 AI 工具配置散落各处 | 中央化配置管理 |
| 每换工具都要重新配置 | 一键部署脚本 |
| AI 工具之间无法协作 | 统一网关接入 |
| Skill 库难以共享和复用 | 中央 Skill 资源库 |

## ✨ 核心功能

```
┌─────────────────────────────────────────────────────────────┐
│                    AgentHub 平台                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐             │
│  │ 工具管理   │  │ 部署中心   │  │ 网关接入   │             │
│  │ OpenCode  │  │ 一键部署   │  │ 微信/QQ   │             │
│  │ Claude   │  │ 容器化     │  │ Telegram  │             │
│  │ Codex    │  │ 脚本化     │  │ 飞书      │             │
│  └───────────┘  └───────────┘  └───────────┘             │
│                                                             │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐             │
│  │ Skill库   │  │ Agent库   │  │ 任务调度   │             │
│  │ 共享技能   │  │ 角色配置   │  │ DAG调度   │             │
│  │ 社区分享   │  │ 工作流     │  │ 并发执行   │             │
│  └───────────┘  └───────────┘  └───────────┘             │
│                                                             │
│  ┌─────────────────────────────────────────┐               │
│  │            多端交互层                    │               │
│  │  🌐 Web    📱 CLI    🖥️ GUI    📟 TUI │               │
│  └─────────────────────────────────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd agenthub
pip install -e .
```

### 2. 初始化（重要！）

**初始化时会自动在用户文件夹创建配置目录：**

```bash
agenthub init
```

初始化后会自动创建以下配置文件夹：

```
C:\Users\<用户名>\.agenthub\
├── config.json      # 主配置文件
├── skills/          # 已安装的 Skills
├── agents/          # Agent 配置文件
├── profile/          # 用户画像
├── projects/         # 项目管理
├── docs/             # 文档
├── secrets/          # 敏感配置 (API密钥等)
├── data/             # 数据存储
├── backup/           # 备份文件
└── logs/             # 运行日志
```

> ⚠️ **默认配置路径**: `C:\Users\<用户名>\.agenthub`
>
> 这是 AgentHub 的**用户配置根目录**，所有用户数据都存放在这里。

### 3. 使用 CLI

```bash
# 查看帮助
agenthub --help

# 列出已安装的 Skills
agenthub skill list

# 安装 Skill
agenthub skill install /path/to/skill

# 搜索 Skill
agenthub skill search github

# 查看 Skill 详情
agenthub skill info github-pr

# 列出可用 Agent
agenthub agent list

# 查看 Agent 状态
agenthub agent status

# 提交任务
agenthub task submit "帮我审查这段代码" --agent claude --priority high

# 列出任务
agenthub task list --status pending

# 查看注册表信息
agenthub registry info
```

### 4. 启动 Web UI

打开浏览器访问：

```
D:\code\github\agenthub\web\工具检测\index.html
```

或启动后端 API 服务：

```bash
# 安装 Web 依赖
cd web/工具检测
pip install -r requirements.txt

# 启动服务
python api.py
# 访问 http://localhost:5174
```

## 📁 目录结构

```
agenthub/
├── 核心/agenthub/            # 🎯 核心源码
│   ├── cli/                  # 📱 CLI 命令行
│   │   ├── main.py          # 主入口
│   │   └── commands/         # 子命令
│   └── core/
│       ├── skill/            # 🛠️ Skill 核心模块
│       ├── agent/            # 🤖 Agent 核心模块
│       ├── memory/           # 🧠 记忆模块
│       └── database/         # 💾 数据库持久化
├── web/                      # 🌐 Web 界面
│   ├── 界面/                 # 主管理界面 (index.html)
│   ├── 后端模块/             # FastAPI 后端
│   └── 工具检测/             # AI 工具检测 API
├── 技能库/                    # 🛠️ 共享技能库
├── 智能体/                    # 🤖 Agent 配置
├── 脚本/                      # 🚀 初始化脚本
├── 测试/                      # 🧪 单元测试
├── 文档/                      # 📚 项目文档
├── 画像/                      # 👤 用户画像
├── 项目/                      # 📁 项目管理
├── 密钥/                      # 🔐 敏感配置
└── 示例/                      # 💡 使用示例
```

## 🌐 公共资源库

AgentHub 内置**公共 Skill 资源库**，来源目录：

```
~/shared-skills/
```

包含 26+ 共享 Skills，分类：

| 分类 | 示例 |
|------|------|
| 开发 | 全栈开发、微信小程序、ADB工具集、支付宝支付 |
| 效率 | 腾讯文档、腾讯问卷、飞书通知、邮件管理 |
| 创意 | PPT制作、Word文档、Excel处理、OCR识别 |
| 研究 | 论文写作工作流、arXiv搜索、百度学术 |
| AI/ML | llama.cpp、vLLM服务、HuggingFace工具 |
| 生活 | 健康Agent、课程表查询、天气查询、待办事项 |

其他公共资源路径：

| 资源 | 路径 |
|------|------|
| 用户画像 | `~/.agenthub/profile/` |
| 项目文档 | `~/projects/` |
| 博客草稿 | `~/blog-drafts/` |
| 知识库 | `~/knowledge/vault/` |
| 服务器备份 | `your-server@example.com:/backup` |

## 🤖 内置 Agent

| Agent | 描述 | 能力 |
|-------|------|------|
| Claude | Anthropic Claude | 代码审查、推理、写作 |
| OpenCode | OpenAI Codex | 代码生成、补全、重构 |
| Codex | GitHub Codex | GitHub 动作、PR 审查 |
| Codefy | 通义灵码 | 阿里云生态、钉钉集成 |

## 🛠️ Skill 示例

一个 Skill 的结构：

```
github-pr/
├── SKILL.md          # Skill 定义（必需）
├── references/       # 参考文档
├── templates/        # 模板文件
└── scripts/          # 自动化脚本
```

SKILL.md 示例：

```yaml
---
name: github-pr
version: 1.0.0
description: GitHub PR 管理工具
author: Xavier
tags: [github, pr, code-review]
triggers: [pr, pull request, github]
dependencies: []
---
```

## 📖 详细文档

- [📋 SPEC.md](SPEC.md) - 完整规范文档
- [📁 目录结构说明](docs/structure.md)
- [🤖 Agent配置指南](agents/)
- [🛠️ Skills技能库](skills/)
- [🌐 Web开发指南](web/)

## 🚀Roadmap

- [x] CLI 命令行工具
- [x] Web 管理界面
- [x] SQLite 持久化
- [x] Skill 注册表
- [x] Agent 调度器
- [x] 公共资源库
- [x] 用户配置文件夹初始化
- [ ] Docker 部署
- [ ] 多 Agent 协作
- [ ] 云端同步
- [ ] 插件系统

## 🤝 参与贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing`)
3. 提交更改 (`git commit -m 'feat: add amazing'`)
4. 推送分支 (`git push origin feature/amazing`)
5. 创建 Pull Request

## 📝 License

MIT License

---

*最后更新：2026-04-26*
