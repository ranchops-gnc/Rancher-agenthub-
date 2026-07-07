# AgentHub Skill 规范 v2.0

> 版本: v2.0 | 更新: 2026-04-29 | 跨工具通用

---

## 1. 概述

AgentHub Skill 规范定义了通用的 skill 格式，支持跨 AI 工具共享。

**支持的工具：**
- OpenCode
- Cursor
- Continue
- Cline / Roo Code
- 其他支持 skill 的 AI 工具

---

## 2. 文件格式

### 2.1 目录结构

```
skills/
├── skill-name/
│   ├── SKILL.md          # 主文件（必需）
│   ├── README.md         # 说明文档（可选）
│   ├── scripts/          # 脚本文件（可选）
│   └── templates/        # 模板文件（可选）
└── another-skill/
    └── SKILL.md
```

### 2.2 SKILL.md 格式

```markdown
---
name: skill-name
description: 简短描述
version: "1.0.0"
triggers: ["触发词1", "触发词2"]
author: "作者名"
license: "MIT"
compatibility: ["opencode", "cursor", "continue"]
---

# Skill 标题

## 触发条件

- 用户提到 xxx 时使用此 skill

## 使用方法

### 步骤 1
...

### 步骤 2
...

## 示例

...
```

---

## 3. YAML Frontmatter 字段

### 3.1 必需字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | Skill 名称（英文，kebab-case） |
| `description` | string | 简短描述（一句话） |

### 3.2 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `version` | string | 版本号（SemVer） |
| `triggers` | string[] | 触发词列表 |
| `trigger` | string[] | 触发词列表（兼容格式） |
| `author` | string | 作者 |
| `license` | string | 许可证 |
| `compatibility` | string[] | 兼容的工具列表 |
| `tags` | string[] | 标签 |
| `dependencies` | string[] | 依赖的其他 skill |

---

## 4. 触发词规范

### 4.1 格式

```yaml
triggers: ["关键词1", "关键词2", "短语"]
```

或

```yaml
trigger:
  - "关键词1"
  - "关键词2"
  - "短语"
```

### 4.2 规则

- 触发词不区分大小写
- 支持中英文
- 支持多个单词的短语
- 优先匹配更长的触发词

---

## 5. 兼容性

### 5.1 工具标识

| 工具 | 标识 |
|------|------|
| OpenCode | `opencode` |
| Cursor | `cursor` |
| Continue | `continue` |
| Cline | `cline` |
| Roo Code | `roo-code` |
| Claude Code | `claude-code` |

### 5.2 兼容性声明

```yaml
compatibility: ["opencode", "cursor", "continue"]
```

如果未声明，默认兼容所有工具。

---

## 6. 跨工具共享

### 6.1 共享目录

```
~/.agenthub/skills/          # 共享 skill 库
```

### 6.2 符号链接

各工具通过符号链接指向共享目录：

```bash
# Linux/macOS
ln -s ~/.agenthub/skills/ ~/.config/opencode/skills/

# Windows (PowerShell)
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.config\opencode\skills" -Target "$env:USERPROFILE\.agenthub\skills"
```

---

## 7. 最佳实践

1. **一个 skill 一个目录**：便于管理和共享
2. **使用通用语言**：优先使用英文，支持中文
3. **保持简洁**：SKILL.md 不要太长，复杂内容放到子文件
4. **版本管理**：使用 SemVer 版本号
5. **声明兼容性**：明确支持哪些工具

---

## 8. 示例

### 8.1 简单 Skill

```markdown
---
name: hello
description: 一个简单的示例 skill
triggers: ["你好", "hello"]
---

# Hello Skill

当用户说"你好"或"hello"时，回复问候。

## 回复

"你好！有什么可以帮助你的吗？"
```

### 8.2 复杂 Skill

```markdown
---
name: pdf
description: PDF 文件处理
version: "1.0.0"
triggers: ["pdf", "PDF", "文档"]
compatibility: ["opencode", "cursor"]
---

# PDF 处理

## 功能

- 读取 PDF 内容
- 提取表格
- 合并/拆分 PDF
- 添加水印

## 使用方法

...
```

---

*AgentHub Skill 规范 v2.0*