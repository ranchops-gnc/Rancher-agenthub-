# AgentHub 初始化标准流程 (SOP)

> **适用对象**: 所有接入 AgentHub 的 AI 助手
> **版本**: v1.1 | 更新: 2026-04-28
> **目的**: 标准化 AI 初始化流程，确保 AI 能够正确理解项目并主动修改自身配置

---

## 🎯 核心原则

1. **AgentHub 是 AI 的工作文件夹** — AI 应将 `~/.agenthub` 作为主要工作目录
2. **主动修改自身文档** — AI 读取项目文档后，必须根据自身身份修改对应的 Agent 配置
3. **按需删减** — 不需要的目录应主动删除，保持项目整洁
4. **中文优先** — 中文用户环境下，优先使用中文命名和中文文档

---

## 📋 SOP 流程图

```
┌──────────────────────────────────────────────────────────────┐
│                    AI 初始化 SOP                              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  1️⃣ 读取项目结构   →   2️⃣ 注册 Agent    →   3️⃣ 读取用户画像    │
│         ↓                    ↓                    ↓           │
│  4️⃣ 修改自身配置   →   5️⃣ 清理不需要的目录   →   6️⃣ 开始工作   │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 第一步：读取项目结构

AI 启动后，**立即执行**：

```bash
# 列出 AgentHub 根目录结构
ls -la ~/.agenthub/

# 查看各目录内容
ls -la ~/.agenthub/agents/
ls -la ~/.agenthub/profile/
ls -la ~/.agenthub/memory/
ls -la ~/.agenthub/skills/
```

### 目录结构说明

| 目录 | 用途 | 是否必须 |
|------|------|----------|
| `agents/` | Agent 配置文件 | ✅ 必须 |
| `profile/` | 用户画像 | ✅ 必须 |
| `memory/` | 记忆存储 | ✅ 必须 |
| `skills/` | 已安装 Skills | ✅ 必须 |
| `projects/` | 项目管理 | ⚙️ 可选 |
| `docs/` | 文档 | ⚙️ 可选 |
| `secrets/` | 敏感配置 | ⚙️ 可选 |
| `data/` | 数据存储 | ⚙️ 可选 |
| `backup/` | 备份文件 | ⚙️ 可选 |
| `logs/` | 运行日志 | ⚙️ 可选 |

### ⚠️ 清理规则

**如果以下目录为空或包含占位文件，AI 应主动删除：**
- `projects/` — 如果用户没有项目管理需求
- `docs/` — 如果用户不需要额外文档
- `backup/` — 如果用户不使用备份功能
- `logs/` — 如果用户不查看日志

```bash
# 删除空目录示例
rmdir ~/.agenthub/projects 2>/dev/null || rm -rf ~/.agenthub/projects
rmdir ~/.agenthub/backup 2>/dev/null || rm -rf ~/.agenthub/backup
```

---

## 第二步：注册 Agent

### 检查注册表

读取 `~/.agenthub/agents/registry.json`，确认自己是否已注册：

```bash
cat ~/.agenthub/agents/registry.json
```

### 如果未注册，执行注册

```python
import json
import os
from datetime import datetime

path = os.path.expanduser("~/.agenthub/agents/registry.json")
reg = json.load(open(path)) if os.path.exists(path) else {"agents": {}}

# ===== 根据你的身份填写 =====
my_id = "your-agent-id"           # 例如: dev-agent, life-agent
my_signature = f"[{my_id}]"      # 必须与 id 一致
my_display_name = "你的名字"        # 中文显示名
my_type = "specialist"            # router 或 specialist
my_capabilities = ["coding"]      # 你的能力列表
my_platform = "opencode"           # 当前使用的平台
my_note = "中文描述你的职责"

if my_id not in reg["agents"]:
    reg["agents"][my_id] = {
        "id": my_id,
        "signature": my_signature,
        "display_name": my_display_name,
        "type": my_type,
        "first_seen": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_active": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "capabilities": my_capabilities,
        "platform": my_platform,
        "status": "active",
        "note": my_note
    }
    json.dump(reg, open(path, "w"), ensure_ascii=False, indent=2)
    print(f"✅ [{my_id}] 注册成功")
else:
    print(f"ℹ️  [{my_id}] 已注册，更新 last_active")
    reg["agents"][my_id]["last_active"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump(reg, open(path, "w"), ensure_ascii=False, indent=2)
```

### 修改对应的 Agent 配置文件

注册后，必须修改对应的 Agent 配置文件（如果存在）：

```bash
# 例如你注册为 dev-agent，则修改
cat ~/.agenthub/agents/dev-agent/AGENT.md
# 或 ~/.agenthub/agents/dev-agent.md
```

**必须修改的内容：**
1. **身份描述** — 改为符合你实际能力的描述
2. **语言风格** — 根据用户偏好设置（中文用户用中文）
3. **触发词** — 设置你希望被触发的关键词
4. **技能绑定** — 绑定你实际要使用的 Skills

### 注册到记忆系统（必须！）

注册 Agent 后，还必须在记忆系统中注册，获得个人工作记忆空间：

```python
import os
from pathlib import Path

AGENTHUB_DIR = os.path.expanduser("~/.agenthub")
memory_dir = os.path.join(AGENTHUB_DIR, "memory")
os.makedirs(memory_dir, exist_ok=True)

# 创建 AI 的工作记忆目录
agent_memory_dir = os.path.join(memory_dir, "agents", my_id)
for subdir in ["daily", "longterm", "projects", "learned"]:
    Path(agent_memory_dir, subdir).mkdir(parents=True, exist_ok=True)

# 注册到记忆系统
memory_registry_path = os.path.join(memory_dir, "agent_registry.json")
if os.path.exists(memory_registry_path):
    with open(memory_registry_path, 'r') as f:
        memory_registry = json.load(f)
else:
    memory_registry = {"agents": {}}

memory_registry['agents'][my_id] = {
    "id": my_id,
    "memory_dir": agent_memory_dir,
    "registered_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "last_active": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "status": "active"
}

with open(memory_registry_path, 'w') as f:
    json.dump(memory_registry, f, ensure_ascii=False, indent=2)

print(f"✅ 记忆系统注册完成: {agent_memory_dir}")
```

**记忆目录结构：**
```
~/.agenthub/memory/agents/<your-agent-id>/
├── daily/        # 每日笔记 (daily/YYYY-MM-DD.md)
├── longterm/     # 长期记忆 (preferences.md, identity.md)
├── projects/     # 项目记忆 (<project-name>.md)
└── learned/      # 经验教训 (lessons.md)
```

---

## 第三步：读取用户画像

### 必读文件

```bash
# 1. 身份信息（必须）
cat ~/.agenthub/profile/identity.yaml

# 2. 联系人（如果存在）
ls ~/.agenthub/profile/contacts/
cat ~/.agenthub/profile/contacts/*.yaml 2>/dev/null

# 3. 技能图谱（如果存在）
cat ~/.agenthub/profile/skills.md 2>/dev/null || echo "暂无"
```

### 用户画像示例（中文用户）

```yaml
# ~/.agenthub/profile/identity.yaml
name: 张三
basic:
  gender: 男
  age: 25
  location: 北京
  native_language: 普通话

contact:
  wechat: zhangsan
  email: zhangsan@example.com

personality:
  traits:
    - 喜欢简洁直接的沟通
    - 技术导向
  communication_style: 直接
  mbti: INTJ

preferences:
  aesthetic:
    primary_color: "#c45d2c"
    secondary_color: "#e8a838"
  response_style:
    emoji: true
    language: zh-CN

ai_assistant:
  name: 小智
  style: 专业、简洁
  emoji: 🤖
```

### 根据用户画像调整

AI 应根据用户画像调整：
- **语言** — 中文用户用中文回复
- **风格** — 根据 `communication_style` 调整
- **偏好** — 根据 `preferences.response_style` 调整回复格式

---

## 第四步：修改自身配置

### 修改 Agent 配置文件

找到你的 Agent 配置文件并修改：

```bash
# 列出所有 Agent
ls ~/.agenthub/agents/

# 查看你的 Agent 配置
cat ~/.agenthub/agents/<your-agent-id>/AGENT.md
```

### 必须修改的内容

```markdown
# AGENT.md

## 身份

- **ID**: your-agent-id
- **名称**: 你的中文名称
- **类型**: specialist / router
- **语言**: zh-CN（中文）

## 职责

描述你的具体职责，用中文写。

## 触发词

列出你希望被触发的关键词（中文）：
- "开发"、"编程"、"代码"
- "写代码"、"调试"、"重构"

## 技能

列出你绑定 Skills：
- github
- adb-debug
- browser-bridge

## 工作方式

- 语言：中文
- 回复风格：简洁、直接
- 主动学习：是
```

### 修改示例

假设你注册为 `dev-agent`，原始配置可能不适合你：

```bash
# 查看原始配置
cat ~/.agenthub/agents/dev-agent/AGENT.md

# 根据你的实际能力修改
# 将英文描述改为中文
# 将不匹配的能力改为你的实际能力
# 添加/删除触发词
# 绑定你需要的 Skills
```

### 将自己的核心 Skill 写入共享库（必须！）

初始化时，**必须**将自己的核心 Skill 写入共享库 `~/.agenthub/skills/`，供其他 AI 使用：

```bash
# 创建你的 Skill 目录
SKILLS_DIR=~/.agenthub/skills
mkdir -p $SKILLS_DIR/<your-agent-id>

# 写入 SKILL.md
cat > $SKILLS_DIR/<your-agent-id>/SKILL.md << 'EOF'
---
name: <your-agent-id>
description: 你的 Skill 描述
triggers:
  - "触发词1"
  - "触发词2"
metadata:
  version: "1.0.0"
  author: "[your-agent-id]"
---

# <your-agent-id> Skill

## 功能

描述你的核心功能。

## 使用方法

描述如何使用。
EOF

echo "✅ Skill 已写入共享库: $SKILLS_DIR/<your-agent-id>/"
```

**共享库规则：**
- `~/.agenthub/skills/` 是共享 Skill 库，所有 AI 工具共享
- 优先级高于平台自身 Skill 库
- 每个 AI 应在初始化时写入自己的核心 Skill

---

## 第五步：清理不需要的目录

### 判断标准

| 目录 | 删除条件 |
|------|----------|
| `projects/` | 用户没有提到任何项目 |
| `docs/` | 用户只需要最基本的文档 |
| `backup/` | 用户没有备份需求 |
| `logs/` | 用户不查看日志 |
| `data/` | 用户没有数据存储需求 |

### 清理执行

```bash
# 检查目录是否为空
ls -la ~/.agenthub/projects/
# 如果只有 README.md 或空，删除

rm -rf ~/.agenthub/projects
rm -rf ~/.agenthub/backup
# 保留 logs 目录但清空内容
# rm -rf ~/.agenthub/logs/*

echo "✅ 清理完成"
```

### 用户确认

清理前可以询问用户：

```
我将清理以下不需要的目录：
- projects/（空目录）
- backup/（空目录）

确认删除？ (y/n)
```

---

## 第六步：开始工作

### 完整初始化清单

```
□ 读取项目结构
□ 确认 Agent 注册
□ 读取用户画像
□ 修改自身 Agent 配置
□ 清理不需要的目录
□ 验证初始化完成
```

### 验证命令

```bash
# 验证 AgentHub 可用
agenthub --version

# 验证 Skills 可用
agenthub skill list

# 验证 Agent 注册
cat ~/.agenthub/agents/registry.json | grep your-agent-id

# 验证用户画像
cat ~/.agenthub/profile/identity.yaml | head -20
```

### 首次工作输出

初始化完成后，输出：

```
✅ AgentHub 初始化完成

[your-agent-id] 已就绪
- 用户: 张三
- 语言: 中文
- 工作目录: ~/.agenthub
- 已注册 Skills: 5 个

可以开始工作了。
```

---

## 📁 目录中文命名建议

| 英文目录 | 中文建议 | 说明 |
|----------|----------|------|
| `profile/` | `用户画像/` | 用户信息目录 |
| `profile/contacts/` | `用户画像/联系人/` | 联系人目录 |
| `profile/health/` | `用户画像/健康/` | 健康记录 |
| `profile/growth/` | `用户画像/成长/` | 成长轨迹 |
| `memory/` | `记忆/` | 记忆存储 |
| `memory/short_term/` | `记忆/短期/` | 短期记忆 |
| `memory/long_term/` | `记忆/长期/` | 长期记忆 |
| `skills/` | `技能库/` | Skills 目录 |

### 使用中文目录

如果用户偏好中文，可以创建中文别名：

```bash
# 创建中文目录（可选）
mkdir -p ~/.agenthub/用户画像
mkdir -p ~/.agenthub/记忆/短期
mkdir -p ~/.agenthub/记忆/长期

# 在配置中指定中文路径
```

---

## 🔧 常见问题

### Q: registry.json 不存在？

```bash
mkdir -p ~/.agenthub/agents
echo '{"agents": {}}' > ~/.agenthub/agents/registry.json
```

### Q: profile/ 目录为空？

```bash
# 运行初始化向导
agenthub init
# 或手动创建
mkdir -p ~/.agenthub/profile/contacts
```

### Q: 如何确认用户语言偏好？

读取 `~/.agaghub/profile/identity.yaml` 中的：
```yaml
preferences:
  response_style:
    language: zh-CN  # 中文
```

---

## 📚 相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| AI 使用指南 | `~/.agenthub/docs/for-ai/AI_GUIDE.md` | 完整 AI 初始化流程 |
| Skill 规范 | `~/.agenthub/docs/design/skill-format.md` | Skill 编写规范 |
| Agent 规范 | `~/.agenthub/docs/design/agent-format.md` | Agent 配置规范 |
| 用户画像规范 | `~/.agenthub/docs/for-ai/user-profile-spec.md` | 画像格式说明 |

---

## ✅ 检查清单

初始化完成后，AI 应确认：

- [ ] 自己已在 `registry.json` 注册
- [ ] 已读取用户画像 `identity.yaml`
- [ ] 已根据用户偏好调整自身配置
- [ ] **已将核心 Skill 写入共享库 `~/.agenthub/skills/`**
- [ ] 已删除不需要的空目录
- [ ] 可以正常执行 `agenthub` 命令
- [ ] 首次输出时告知用户初始化状态

---

*本文档版本: v1.0 | 更新: 2026-04-28*
*本文档由 AgentHub SOP 标准化流程定义*
