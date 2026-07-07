# AgentHub 安装脚本

> 统一 AI 工具的 Skill · Agent · 画像 · 记忆系统 四大共享生态

## 一键安装（推荐）

```bash
curl -fsSL https://raw.githubusercontent.com/xuanyuanluoxue/AgentHub/main/misc/install.sh | bash
```

## 功能

| 选项 | 说明 |
|------|------|
| `1` | 安装 AgentHub |
| `2` | 更新 AgentHub |
| `3` | 重新安装 |
| `4` | 卸载 AgentHub |
| `5` | 打开配置目录 |
| `6` | 退出 |

## 使用方式

### 交互模式（有终端）

```bash
curl -fsSL .../install.sh | bash
# 显示菜单，选择操作
```

### 下载到本地

```bash
curl -fsSL .../install.sh -o agenthub_install.sh
bash agenthub_install.sh
```

## 安装位置

```
~/.agenthub/   # Linux/macOS/WSL
%USERPROFILE%\.agenthub\   # Windows
```

## 安装后

```bash
agenthub --help     # 查看帮助
```