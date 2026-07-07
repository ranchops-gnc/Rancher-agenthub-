# AgentHub 命令行工具设计 (`as`)

> AgentHub 命令行工具设计文档

## 概述

`as` 是 AgentHub 的命令行工具，用于管理 AI 工具、部署、配置和网关。

## 安装

```bash
# Linux/macOS/WSL
curl -fsSL https://raw.githubusercontent.com/xuanyuanluoxue/AgentHub/main/scripts/install.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/xuanyuanluoxue/AgentHub/main/scripts/install.ps1 | iex
```

## 命令结构

```
as [OPTIONS] <command> [args]
```

## 全局选项

| 选项 | 说明 |
|------|------|
| `-h, --help` | 显示帮助 |
| `-v, --version` | 显示版本 |
| `-c, --config <path>` | 指定配置文件 |
| `-d, --debug` | 调试模式 |

## 命令

### init - 初始化

```bash
as init [OPTIONS]

选项:
  --template <name>    模板名称 (default/template/minimal)
  --dir <path>         目标目录
  --force              强制初始化
```

### list - 列出工具

```bash
as list [OPTIONS]

选项:
  --installed          仅显示已安装
  --available          仅显示可安装
  --format <format>    输出格式 (table/json/yaml)
```

### install - 安装工具

```bash
as install <tool> [OPTIONS]

支持的工具:
  opencode              OpenCode AI 编程助手
  openclaw              OpenClaw Agent 框架
  codebuddy             CodeBuddy 代码助手
  claude                Claude Desktop
  cursor                Cursor AI 编辑器
  hermes                Hermes 终端助手

选项:
  --version <ver>      指定版本
  --config <path>      配置文件路径
  --force              强制安装
```

### config - 配置管理

```bash
as config <action> [OPTIONS]

操作:
  get <key>            获取配置值
  set <key> <value>    设置配置值
  list                 列出所有配置
  edit                 编辑配置文件

示例:
  as config get global.editor
  as config set global.theme dark
  as config edit
```

### skill - Skill 管理

```bash
as skill <action> [OPTIONS]

操作:
  list                 列出已安装的 Skills
  search <query>       搜索 Skill
  install <name>       安装 Skill
  uninstall <name>     卸载 Skill
  update <name>        更新 Skill
  info <name>          查看 Skill 信息

示例:
  as skill list
  as skill search github
  as skill install dev-agent
```

### gateway - 网关管理

```bash
as gateway <action> [OPTIONS]

操作:
  list                 列出已配置的网关
  add <name>           添加网关
  remove <name>        移除网关
  status <name>       查看网关状态
  start <name>         启动网关
  stop <name>          停止网关

支持的网关:
  wechat               微信网关
  qq                   QQ 网关
  feishu               飞书网关
  telegram             Telegram 网关
  discord              Discord 网关

示例:
  as gateway list
  as gateway add wechat
  as gateway status feishu
```

### deploy - 部署

```bash
as deploy <tool> [OPTIONS]

选项:
  --env <env>          环境 (dev/staging/prod)
  --host <host>        目标主机
  --method <method>    部署方式 (ssh/docker/local)

示例:
  as deploy opencode --env prod
  as deploy hermes --host 192.168.1.100 --method ssh
```

### sync - 同步配置

```bash
as sync [OPTIONS]

选项:
  --to <target>        同步到目标
  --from <source>      从源同步
  --dry-run            模拟运行

示例:
  as sync --to github
  as sync --from opencode --to openclaw
```

## 配置文件

默认配置文件: `~/.agent-system/config.yaml`

```yaml
global:
  editor: vim
  theme: dark
  debug: false

tools:
  opencode:
    enabled: true
    config_path: ~/.config/opencode
  openclaw:
    enabled: true
    config_path: ~/.openclaw

gateways:
  feishu:
    enabled: true
    app_id: xxx
    app_secret: xxx

sync:
  auto_sync: true
  interval: 3600
```

## 退出码

| 退出码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 参数错误 |
| 3 | 配置错误 |
| 4 | 网络错误 |
| 5 | 权限错误 |

---

*最后更新：2026-04-26*
