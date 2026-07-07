# 支持的 AI 工具

> AgentHub 支持管理的 AI 工具列表

## 工具列表

| 工具 | 类型 | 配置文件 | 状态 |
|------|------|----------|------|
| OpenCode | 编程助手 | `~/.config/opencode/` | ✅ 已支持 |
| OpenClaw | Agent 框架 | `~/.openclaw/` | ✅ 已支持 |
| CodeBuddy | 代码助手 | `~/.codebuddy/` | 🔜 计划中 |
| Claude Desktop | 对话助手 | `~/.claude/` | 🔜 计划中 |
| Cursor | AI 编辑器 | `~/.cursor/` | 🔜 计划中 |
| Hermes | 终端助手 | `~/.hermes/` | 🔜 计划中 |

## OpenCode

### 简介
OpenCode 是一个 AI 编程助手，支持多种编程语言和 IDE。

### 配置文件
```json
{
  "opencode": {
    "model": "minimax-cn-coding-plan/MiniMax-M2.7",
    "api_key": "xxx",
    "theme": "dark"
  }
}
```

### 常用命令
```bash
# 启动
opencode

# 查看帮助
opencode --help

# 配置文件位置
~/.config/opencode/
```

---

## OpenClaw

### 简介
OpenClaw 是一个 AI Agent 框架，支持多 Agent 协作和自定义工作流。

### 配置文件
```json
{
  "openclaw": {
    "gateway_port": 18789,
    "dashboard": "http://127.0.0.1:18789"
  }
}
```

### 常用命令
```bash
# 启动
openclaw

# 查看状态
openclaw status

# 配置文件位置
~/.openclaw/
```

---

## CodeBuddy

### 简介
CodeBuddy 是一个轻量级 AI 代码助手。

### 配置文件
```json
{
  "codebuddy": {
    "server": "https://api.codebuddy.com",
    "token": "xxx"
  }
}
```

### 常用命令
```bash
# 启动
codebuddy

# 配置文件位置
~/.codebuddy/
```

---

## Claude Desktop

### 简介
Claude Desktop 是 Anthropic 官方桌面应用。

### 配置文件
```json
{
  "claude": {
    "api_key": "xxx",
    "model": "claude-3-opus"
  }
}
```

### 配置文件位置
- macOS: `~/.claude/`
- Windows: `%APPDATA%/Claude/`

---

## Cursor

### 简介
Cursor 是一个 AI 代码编辑器，基于 VS Code。

### 配置文件
```json
{
  "cursor": {
    "api_key": "xxx",
    "mode": "pro"
  }
}
```

### 配置文件位置
- macOS: `~/.cursor/`
- Windows: `%APPDATA%/Cursor/`
- Linux: `~/.cursor/`

---

## Hermes

### 简介
Hermes 是一个终端 AI 助手，支持多工具集成。

### 配置文件
```json
{
  "hermes": {
    "provider": "minimax",
    "model": "MiniMax-M2.7"
  }
}
```

### 常用命令
```bash
# 启动
hermes

# 查看帮助
hermes --help

# 配置文件位置
~/.hermes/
```

---

*最后更新：2026-04-26*
