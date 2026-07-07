# AgentHub AI 使用指南

> ⚠️ **AI 必读** | 版本: v3.1 | 更新: 2026-04-28
> **首次使用本项目前，必须先完成「初始化 SOP」！**
>
> 📋 **完整初始化流程请参阅**: [INITIALIZATION_SOP.md](./INITIALIZATION_SOP.md)

---

## 🚀 快速初始化（必须执行）

任何 AI 首次启动时，**立即按顺序执行**以下步骤，禁止跳过：

### Step 1 — 读取项目结构

```bash
ls -la ~/.agenthub/
ls -la ~/.agenthub/agents/
ls -la ~/.agenthub/profile/
```

### Step 2 — 注册自己

读取 `~/.agenthub/agents/registry.json`，若自己未在其中，执行注册：

```python
import json, os
from datetime import datetime

path = os.path.expanduser("~/.agenthub/agents/registry.json")
os.makedirs(os.path.dirname(path), exist_ok=True)
reg = json.load(open(path)) if os.path.exists(path) else {"agents": {}}

# ===== 根据你的身份填写 =====
my_id = "your-agent-id"           # 例如: dev-agent
my_signature = f"[{my_id}]"
my_display_name = "你的中文名"
my_type = "specialist"            # router 或 specialist
my_capabilities = ["coding"]      # 你的能力
my_platform = "opencode"           # 当前平台
my_note = "中文描述你的职责"

if my_id not in reg["agents"]:
    reg["agents"][my_id] = {
        "id": my_id, "signature": my_signature, "display_name": my_display_name,
        "type": my_type, "first_seen": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_active": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "capabilities": my_capabilities, "platform": my_platform,
        "status": "active", "note": my_note
    }
    json.dump(reg, open(path,"w"), ensure_ascii=False, indent=2)
    print(f"✅ [{my_id}] 注册成功")
else:
    print(f"ℹ️  [{my_id}] 已注册")
```

### Step 2.5 — 在记忆系统中注册（必须！）

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

### Step 3 — 读取用户画像

```bash
cat ~/.agenthub/profile/identity.yaml
cat ~/.agenthub/profile/contacts/*.yaml 2>/dev/null || echo "暂无联系人"
```

### Step 4 — 修改自身 Agent 配置

注册后，**必须**修改对应的 Agent 配置文件：

```bash
# 查看你的 Agent 配置
cat ~/.agenthub/agents/<your-agent-id>/AGENT.md

# 根据你的实际能力和用户偏好修改：
# 1. 身份描述 → 改为中文，符合你的实际能力
# 2. 语言风格 → 中文用户用中文
# 3. 触发词 → 设置你希望被触发的关键词
# 4. 技能绑定 → 绑定你实际要使用的 Skills
```

### Step 5 — 清理不需要的目录

如果以下目录为空或只有占位文件，**应主动删除**：

```bash
# 删除空目录示例
rm -rf ~/.agenthub/projects   # 如果没有项目管理需求
rm -rf ~/.agenthub/backup     # 如果没有备份需求
rm -rf ~/.agenthub/docs       # 如果不需要额外文档
```

### Step 6 — 确认初始化完成

```bash
# 验证 AgentHub 可用
agenthub --version

# 验证 Skills
agenthub skill list

# 验证 Agent 注册
cat ~/.agenthub/agents/registry.json | grep your-agent-id
```

**完成后输出初始化状态，告知用户你已就绪。**

---

## 🎯 核心原则

1. **AgentHub 是 AI 的工作文件夹** — 使用 `~/.agenthub` 作为主要工作目录
2. **主动修改自身文档** — 读取项目文档后，必须根据自身身份修改对应的 Agent 配置
3. **按需删减** — 不需要的目录应主动删除，保持项目整洁
4. **中文优先** — 中文用户环境下，优先使用中文命名和中文文档

---

## 👤 用户画像

**必读文件**: `~/.agenthub/profile/identity.yaml`

```yaml
name: 用户名
basic:
  email: user@example.com
  location: 城市
personality:
  communication_style: 直接/委婉
preferences:
  aesthetic:
    primary_color: "#c45d2c"
```

**读取方式**:
```python
import yaml
with open("~/.agenthub/profile/identity.yaml") as f:
    profile = yaml.safe_load(f)
```

## 🛠️ Skills 使用

Skills 是可复用的功能模块，通过**触发词**自动加载。

### Skill 加载优先级

AgentHub 支持**多源 Skill**，加载顺序如下：

| 优先级 | 来源 | 说明 |
|--------|------|------|
| **高** | `~/.agenthub/skills/` | **共享 Skill 库**，所有 AI 工具共享，优先使用 |
| 低 | 平台自身 Skill 库 | 各 AI 工具自带的 Skill |

**原则：共享 Skill 库优先级高于平台自身 Skill 库。**

> 例如：OpenCode 自带某个 Skill，但 AgentHub 共享 Skill 库中也有同名的，优先使用共享库版本。

### 触发词示例

| Skill | 触发词 | 功能 |
|-------|--------|------|
| github-pr | "github pr"、"推送" | GitHub PR 管理 |
| adb-debug | "adb"、"调试" | Android 调试 |
| browser-bridge | "浏览器"、"打开网页" | 浏览器自动化 |

### 加载 Skill

```python
from agenthub.core.skill.registry import SkillRegistry

registry = SkillRegistry()
skill = registry.get("github-pr")  # 按名称获取
results = registry.find_by_trigger("用户说想管理pr")  # 按触发词查找
```

## 🤖 Agents

Agents 是专业角色配置，定义了该 AI 的职责和技能绑定。

### 内置 Agents

| Agent | 类型 | 职责 |
|-------|------|------|
| main-agent | router | 总调度入口 |
| dev-agent | specialist | 开发任务 |
| life-agent | specialist | 生活服务 |
| ops-agent | specialist | 运营任务 |

### 路由规则

```
用户输入 → 触发词匹配 → 选择 Agent → 执行 Skill → 返回结果
```

## 💾 记忆系统

AgentHub 提供多层记忆，AI **必须主动写入**重要信息。

### 为什么 AI 要主动写记忆？

1. **会话重启后恢复上下文** — AI 每次会话都"失忆"，记忆文件是唯一连续性
2. **跨工具共享** — 写入 `~/.agenthub/memory/` 的内容对所有 AI 工具可见
3. **用户无需重复说明** — 记住的偏好、项目信息无需用户再次告知

### 记忆目录结构

```
~/.agenthub/memory/agents/<your-agent-id>/
├── daily/                    # 每日笔记 (YYYY-MM-DD.md)
├── longterm/                 # 长期记忆
│   ├── preferences.md        # 用户偏好
│   └── identity.md           # 身份信息
├── projects/                 # 项目记忆 (<project-name>.md)
└── learned/                   # 经验教训 (lessons.md)
```

### 何时必须写记忆？

| 场景 | 示例 | 写入位置 |
|------|------|----------|
| 用户明确偏好 | "我喜欢简洁的代码" | `longterm/preferences.md` |
| 项目关键信息 | "这个项目用 Python 3.11" | `projects/<name>.md` |
| 重要决策 | "用户选择方案A" | `projects/<name>.md` |
| 错误教训 | "上次这个API失败了" | `learned/lessons.md` |
| 每日工作 | 完成了哪些任务 | `daily/YYYY-MM-DD.md` |

### 写入示例

> **重要**: 写入记忆时必须带上你的署名 `[your-agent-id]`

```python
# 写入用户偏好
preferences_file = os.path.join(agent_memory_dir, "longterm/preferences.md")
with open(preferences_file, "a", encoding="utf-8") as f:
    f.write("\n\n## [your-agent-id] 记录")
    f.write("\n- 用户喜欢简洁的代码风格")

# 写入项目记忆
project_file = os.path.join(agent_memory_dir, "projects/agenthub.md")
with open(project_file, "a", encoding="utf-8") as f:
    f.write("\n\n## [your-agent-id] 记录")
    f.write("\n## 2026-04-28: 决定使用 GitHub 模式")

# 写入每日笔记
daily_file = os.path.join(agent_memory_dir, "daily/2026-04-28.md")
with open(daily_file, "w", encoding="utf-8") as f:
    f.write(f"# 2026-04-28 工作日志\n\n## [your-agent-id]\n\n## 完成\n- 任务A\n\n## 待办\n- [ ] 任务B")
```

### 文字优先原则

> **文字 > 大脑** 📝

- "mental notes" 不会在会话重启后存活
- 如果想记住什么，就写下来
- "记住这个" → 立即更新相关记忆文件

---

## 🌟 Skill 沉淀推荐

> **推荐功能，非强制** — 如果你在工作中发现可以复用的模式或工作流，可以考虑沉淀为 Skill

### 何时考虑沉淀？

| 场景 | 示例 | 是否建议 |
|------|------|----------|
| 重复性任务 | 每次都要执行相似的步骤 | ✅ 建议 |
| 复杂工作流 | 多步骤组合的固定流程 | ✅ 建议 |
| 一次性任务 | 用完即弃 | ❌ 不建议 |

### 沉淀流程

```
发现可复用模式 → 记录到 learned/ → 如果重复 3 次以上 → 创建/更新 Skill
```

### Skill 存放位置

```
~/.agenthub/skills/           # 共享 Skill 库（所有 AI 工具共享）
```

**共享 Skill 库规则：**
- 所有 AI 工具都可以读取和使用
- 优先级高于平台自身 Skill 库
- 新增/修改 Skill 应放在此目录

### 示例

```python
# 如果发现某个模式重复多次，写入经验教训
lessons_file = os.path.join(agent_memory_dir, "learned/lessons.md")
with open(lessons_file, "a", encoding="utf-8") as f:
    f.write("\n\n## [your-agent-id] 记录")
    f.write("\n## 2026-04-28")
    f.write("\n- **ADB 调试流程**: 这个流程重复了 5 次，建议沉淀为 Skill")

# 如果确定要创建 Skill（可选，非强制）
skill_dir = os.path.join(AGENTHUB_DIR, "skills", "android-debug")
os.makedirs(skill_dir, exist_ok=True)
# 写入 SKILL.md...
```

### 判断标准

```
□ 这个模式重复出现 ≥ 3 次？
□ 其他人也可能用到？
□ 可以用固定步骤描述？

如果以上都是 ✓ → 建议沉淀为 Skill
```

> 沉淀 Skill 是**推荐功能**，不是强制要求。重要的是文字记录，形式可以后续调整。

## 📝 常用命令

```bash
# Skills
agenthub skill list              # 列出 Skills
agenthub skill search <关键词>   # 搜索 Skill

# Agents
agenthub agent list             # 列出 Agents
agenthub agent info <名称>      # 查看详情

# 记忆
agenthub memory stats           # 记忆统计
agenthub memory search <关键词>  # 搜索记忆
```

## 🔑 核心规范

### 1. 优先读取用户画像

首次对话应读取 `~/.agenthub/profile/identity.yaml` 了解用户。

### 2. 主动记忆重要信息

用户告诉的偏好、项目信息等，应主动写入记忆系统。

### 3. 复用 Skills

遇到常见任务，先搜索是否有对应 Skill，避免重复造轮子。

### 4. 遵循触发词机制

Skill 通过触发词激活，不要硬编码 Skill 逻辑。

### 5. 尊重用户隐私

用户画像和记忆中的敏感信息不要外泄。

## 🤖 Agent 注册与署名

### 注册表

所有 AI Agent 都在 `~/.agenthub/agents/registry.json` 注册：

```json
{
  "agents": {
    "dev-agent": {
      "id": "dev-agent",
      "signature": "[dev]",
      "display_name": "Dev Agent",
      "type": "specialist",
      "capabilities": ["coding", "fullstack"],
      "status": "active"
    }
  }
}
```

### 署名格式

所有 AI 输出必须带署名，格式为 `[agent-id]`：

```
[hermes] 已完成记忆系统更新。
[dev] 开始处理开发任务...
[life] 今日课程：无课
```

### 新 AI 注册流程

1. 读取 `~/.agenthub/agents/registry.json`
2. 检查自己是否已注册
3. 未注册则添加自己的身份
4. 每次会话更新 `last_active`

详见 `~/.agenthub/docs/for-ai/onboarding-protocol.md`

---

## 📁 文件位置

| 文件 | 路径 |
|------|------|
| 用户画像 | `~/.agenthub/profile/identity.yaml` |
| Skills 注册表 | `~/.agenthub/registry.json` |
| Agent 注册表 | `~/.agenthub/agents/registry.json` |
| 记忆存储 | `~/.agenthub/memory/` |
| Agent 模板 | `~/.agenthub/agents/templates/proactive/` |
| 配置文件 | `~/.agenthub/config.yaml` |

---

## 📚 Agent 模板（Proactive Agent 系列）

AgentHub 提供源自 **proactive-agent (Hal Labs)** 的专业模板，位于 `agents/templates/proactive/`：

| 模板 | 说明 |
|------|------|
| `SOUL.md` | Agent 身份与原则定义 |
| `AGENTS.md` | Agent 操作规则与工作流 |
| `HEARTBEAT.md` | 定期自检清单（安全/自我修复/主动） |
| `USER.md` | 用户信息模板 |
| `MEMORY.md` | 长期记忆模板 |
| `ONBOARDING.md` | 新用户初始化向导 |
| `TOOLS.md` | 工具配置与笔记 |

这些模板帮助 Agent 实现：
- **主动** — 不等待指令，主动创造价值
- **持久** — 通过记忆系统跨会话学习
- **安全** — 定期自检，防止prompt注入

---

*本文档由 AgentHub 自动生成，v2.0 新增 Agent 注册与模板支持。*
