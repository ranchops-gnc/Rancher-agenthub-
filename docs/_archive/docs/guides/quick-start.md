# 快速开始

## 环境要求

- Git
- 文本编辑器（VS Code 等）

## 安装步骤

### 1. Clone 仓库

```bash
git clone https://github.com/xuanyuanluoxue/AgentHub.git
cd agent-system
```

### 2. 初始化配置

```bash
# 复制模板文件
cp profile/template/* profile/

# 编辑你的身份信息
vim profile/identity.md
```

### 3. 配置 AI 工具

在你的 AI 工具中设置以下配置：

```
配置根目录: /path/to/agent-system
```

### 4. 开始使用

现在你可以让 AI 工具读取 `profile/` 下的文件来了解你的信息。

## 目录用途

| 目录 | 用途 |
|------|------|
| `profile/` | 存放你的个人信息 |
| `skills/` | 存放可复用的技能 |
| `agents/` | 配置 AI Agent 角色 |
| `projects/` | 管理项目待办 |
| `secrets/` | 存放敏感信息（不传 Git） |

## Git 提交方法

### 查看当前状态
```bash
cd agenthub
git status
```

### 查看改动内容
```bash
git diff                    # 查看所有改动
git diff --stat             # 简洁统计
git diff 文件路径            # 查看特定文件
```

### 暂存并提交
```bash
git add .                   # 暂存所有改动
git add 文件路径             # 暂存特定文件
git commit -m "提交描述"      # 提交
```

### 推送到 GitHub
```bash
git push                    # 推送到 origin/main
```

### 常用操作
```bash
git log --oneline -5        # 查看最近5条提交
git branch -a               # 查看所有分支
git checkout 分支名         # 切换分支
git restore .               # 撤销所有未暂存改动
```

### 工作流示例
```bash
# 1. 查看状态
git status

# 2. 查看改动
git diff

# 3. 暂存需要的文件
git add 核心/agenthub/cli/commands/skill.py

# 4. 提交（写清楚做了什么）
git commit -m "feat: 新增 skill 命令行工具"

# 5. 推送
git push -u origin main
```

---

## 下一步

- 阅读 [SPEC.md](SPEC.md) 了解完整规范
- 阅读 [agents/router.md](agents/router.md) 了解路由规则
- 查看 [skills/](skills/) 了解可用技能

---

*最后更新：2026-04-26*
