# Skill 格式规范 v1.0

> 版本: v1.0 | 更新: 2026-04-26

## 概述

Skill 是 AgentHub 的核心扩展单元，每个 Skill 是一个自包含的功能模块，可被多个 AI 工具共享使用。

## 目录结构

```
skill-name/                  # Skill 根目录（英文 kebab-case）
├── SKILL.md                 # ★ 核心定义（必需）
├── README.md                # 使用文档（可选）
├── scripts/                 # 执行脚本
│   ├── install.sh          # 安装脚本
│   ├── validate.sh         # 验证脚本
│   └── *.py                # Python 工具脚本
├── references/             # 参考资料
│   └── *.md
├── templates/               # 模板文件
│   └── *.md
└── assets/                  # 资源文件
    └── *
```

## SKILL.md 格式

```yaml
---
name: skill-name             # Skill 名称（英文 kebab-case）
version: 1.0.0              # SemVer 格式
description: 简短描述       # 一句话说明
author: 作者名               # 作者
tags:                        # 标签（用于搜索）
  - tag1
  - tag2
category: dev|productivity|ai|system  # 分类
trigger:                     # 触发词/条件
  - "触发词1"
  - "触发词2"
dependencies:                # 依赖（可选）
  - skill-name@^1.0.0
tools:                       # 需要的工具（可选）
  - python
  - git
platform: windows|linux|macos|all  # 支持平台
license: MIT                # 许可证
homepage: https://...       # 主页（可选）
source: https://...         # 源码地址（可选）
---

# Skill 正文（Markdown）

这里是 Skill 的详细说明，可以使用 Markdown 格式。

## 使用方法

描述如何使用这个 Skill。

## 示例

\`\`\`bash
示例命令
\`\`\`

## 注意事项

使用时的注意点。
```

## 字段说明

### 必需字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | Skill 名称，英文 kebab-case，唯一 |
| `version` | string | SemVer 格式，如 `1.0.0` |
| `description` | string | 一句话简短描述 |
| `trigger` | string[] | 触发词数组 |

### 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `author` | string | 作者名 |
| `tags` | string[] | 标签数组 |
| `category` | enum | 分类：dev/productivity/ai/system |
| `dependencies` | string[] | 依赖的其他 Skill（格式：`name@version`） |
| `tools` | string[] | 依赖的工具 |
| `platform` | enum | 支持平台：windows/linux/macos/all |
| `license` | string | 许可证 |
| `homepage` | string | 主页 URL |
| `source` | string | 源码地址 |

## 触发词设计原则

1. **简短**：2-8 个字符
2. **唯一**：避免与常用词重叠
3. **场景化**：体现使用场景

**好的触发词：**
- `adb-debug` - ADB 调试
- `github-pr` - GitHub PR 管理
- `blog-push` - 博客推送

**不好的触发词：**
- `debug` - 太通用
- `github` - 只是工具名，缺少动作
- `推送` - 中文，英文工具可能不识别

## 分类规范

| 分类 | 说明 | 示例 |
|------|------|------|
| `dev` | 开发相关 | 代码审查、调试 |
| `productivity` | 效率工具 | 日程、笔记 |
| `ai` | AI 相关 | 提示词、模型调用 |
| `system` | 系统管理 | 文件、进程 |

## 版本管理

使用 [SemVer](https://semver.org/) 格式：

- `1.0.0` - 正式版
- `0.1.0` - 开发版
- `1.0.0-beta.1` - 测试版

**版本范围：**
- `^1.0.0` - 兼容 1.x.x
- `~1.0.0` - 兼容 1.0.x
- `>=1.0.0 <2.0.0` - 范围限定

## 依赖解析

### 依赖格式

```yaml
dependencies:
  - github-pr@^1.0.0      # 必需
  - optional-skill@^2.0.0  # 可选（标记待定）
```

### 循环依赖处理

- **禁止**：Skill 不能依赖自己（直接循环）
- **检测**：安装时检测循环依赖并报错
- **解决**：重新设计依赖结构

## 安装流程

1. **解析**：读取 SKILL.md，提取元数据
2. **验证**：检查依赖是否满足
3. **下载**：复制到 `~/.agenthub/skills/`
4. **安装**：运行 `scripts/install.sh`（如有）
5. **注册**：添加到本地注册表

## 存储位置

```
~/.agenthub/                  # 用户本地数据
├── skills/                   # 已安装的 Skill
│   ├── github-pr/
│   │   └── SKILL.md
│   └── blog-push/
│       └── SKILL.md
├── registry.json            # 本地注册表
└── skills_cache/           # 缓存目录
```

## 注册表格式

```json
{
  "skills": {
    "github-pr": {
      "name": "github-pr",
      "version": "1.2.0",
      "path": "~/.agenthub/skills/github-pr",
      "installed_at": "2026-04-26T10:00:00Z",
      "source": "local"
    }
  },
  "index_updated_at": "2026-04-26T10:00:00Z"
}
```

## 多工具兼容性

Skill 可被以下工具使用：

| 工具 | 支持度 | 说明 |
|------|--------|------|
| OpenCode | ✅ | 通过 `~/.config/opencode/skills/` |
| OpenClaw | ✅ | 通过 `~/.openclaw/skills/` |
| Claude Code | ✅ | 通过 `~/.claude/skills/` |
| Cursor | ✅ | 通过 `~/.cursor/skills/` |
| Hermes | ✅ | 通过 `~/.hermes/skills/` |

## 示例

### 最小 Skill

```yaml
---
name: hello-world
version: 1.0.0
description: Hello World 示例
trigger:
  - "hello"
---

# Hello World

这是一个示例 Skill。

## 使用

说 "hello" 触发。
```

### 完整 Skill

```yaml
---
name: github-pr-manager
version: 1.0.0
description: GitHub Pull Request 管理工具
author: Xavier
tags:
  - github
  - pr
  - code-review
category: dev
trigger:
  - "github pr"
  - "pr管理"
dependencies:
  - github-cli@^1.0.0
tools:
  - gh
  - git
platform: all
license: MIT
homepage: https://github.com/xuanyuanluoxue/AgentHub
source: https://github.com/xuanyuanluoxue/AgentHub
---

# GitHub PR Manager

管理 GitHub Pull Requests 的 Skill。

## 功能

- 列出待审核的 PR
- 创建 PR
- 查看 PR 状态

## 使用方法

\`\`\`bash
# 列出 PR
agenthub pr list

# 创建 PR
agenthub pr create --title "xxx" --body "xxx"
\`\`\`
```

---

*本文档由 AgentHub 自动生成*
