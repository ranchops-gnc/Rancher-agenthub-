# 记忆系统设计 v1.1

> 版本: v1.1 | 更新: 2026-04-27
> **参考设计**: Hermes Agent 记忆系统

## 概述

AgentHub 记忆系统为 AI 工具提供持久化、多层级的记忆能力，让 AI 能够跨越会话持续学习和记忆用户偏好。

> 本设计**参考 Hermes Agent 的记忆架构**，结合 AgentHub 的跨平台目标进行优化。

---

## 🤖 Agent 注册与署名

AgentHub 在 v1.1 中新增了 **Agent 注册与署名系统**，让多个 AI 可以协同工作并相互识别。

### 目录结构

```
memory/
├── agents/                    # ★ v1.1 新增：Agent 注册表
│   ├── registry.json          # 成员列表（所有已注册 AI）
│   ├── registry-meta.json     # 元数据
│   ├── onboarding-protocol.md # 新 AI 初始化协议
│   └── templates/
│       └── agent-card-template.json  # 身份卡模板
├── hot/                      # 短期记忆（会话级）
├── cold/                      # 中期记忆（7-30天）
├── archive/                   # 归档记忆
├── memories/                 # 核心记忆
│   ├── MEMORY.md            # 重要事实（用 § 分隔）
│   └── USER.md              # 用户画像简要
└── retrieval/                # 检索引擎
```

### 署名格式

所有 AI 输出必须带署名，格式为 `[agent-id]`：

```
[hermes] 已完成记忆系统更新。
[dev] 开始处理开发任务...
[life] 今日课程：无课
```

### 注册流程

1. 读取 `memory/agents/registry.json`
2. 检查自己是否已注册
3. 未注册则添加自己的身份卡
4. 每次会话更新 `last_active`

### Agent 模板

源自 **proactive-agent (Hal Labs)** 的专业模板：

| 模板 | 说明 |
|------|------|
| `SOUL.md` | Agent 身份与原则定义 |
| `AGENTS.md` | Agent 操作规则与工作流 |
| `HEARTBEAT.md` | 定期自检清单 |
| `USER.md` | 用户信息模板 |
| `MEMORY.md` | 长期记忆模板 |

详见 `~/.agenthub/agents/onboarding-protocol.md`

---

## 🏗️ 架构设计

### 多层记忆模型（参考 Hermes）

```
┌─────────────────────────────────────────────────┐
│                   上下文窗口                      │
│            (自动压缩，超限裁剪)                   │
├─────────────────────────────────────────────────┤
│                  Hot Memory                      │
│          (当前会话的活跃信息)                     │
├─────────────────────────────────────────────────┤
│                 Cold Memory                      │
│           (近期重要记忆，7-30天)                  │
├─────────────────────────────────────────────────┤
│                  Archive                         │
│            (归档记忆，长期存档)                   │
└─────────────────────────────────────────────────┘
```

### Hermes 记忆层级对照

| Hermes 目录 | 说明 | AgentHub 对应 |
|-------------|------|---------------|
| `memory/hot/` | 短期记忆 | `memory/hot/` |
| `memory/cold/` | 中期记忆 | `memory/cold/` |
| `memory/archive/` | 归档 | `memory/archive/` |
| `memories/MEMORY.md` | 重要事实（§ 分隔） | `memory/memories/MEMORY.md` |
| `memories/USER.md` | 用户画像简要 | **`profile/identity.yaml`（完整）** |

---

## 📂 目录结构

```
memory/
├── hot/                    # ★ 短期记忆（会话级）
│   └── session_{id}.json  # 按会话组织
├── cold/                   # ★ 中期记忆（7-30天）
│   ├── facts.yaml          # 事实存储
│   ├── preferences.yaml    # 偏好存储
│   └── interactions/        # 交互历史
├── archive/                 # ★ 归档记忆
│   └── archived_{date}.json
├── memories/               # ★ 核心记忆（参考 Hermes）
│   ├── MEMORY.md          # 重要事实（用 § 分隔段落）
│   └── USER.md             # ⚠️ 用户画像简要说明
└── retrieval/              # 检索引擎
    └── index.json          # 检索索引
```

### 关于 USER.md 的说明

> **重要**: `memories/USER.md` 只是用户画像的**简要说明**，用于快速查阅。
> **完整用户画像信息**请访问 `profile/identity.yaml`。

```
memories/USER.md  ──────简要说明──────►  profile/identity.yaml
       │                                      │
       │  摘要引用                            │ 完整数据
       │                                      │
       ▼                                      ▼
   快速查阅用                           完整信息源
```

### Hermes 的 MEMORY.md 格式示例

```markdown
- skills同步：~/.hermes/skills/ 和 ~/.config/opencode/skills/
§
- 跨AI工作交接文件夹：所有AI工具读写这里进行工作交接
§
- 用户风格偏好：喜欢结构清晰的文件夹分类
§
- 服务器地址：https://your-server.example.com:5245
```

> Hermes 使用 `§` 符号分隔不同的记忆条目，每个条目是一个独立的事实或偏好。

---

## 🔧 核心模块

### 1. 短期记忆 (short_term.py)

```python
class ShortTermMemory:
    """短期记忆 - Hot Memory"""

    def __init__(self, session_id: str, ttl_minutes: int = 60):
        self.session_id = session_id
        self.ttl_minutes = ttl_minutes

    def store(self, key: str, value: Any) -> None:
        """存储短期记忆"""

    def recall(self, key: str) -> Optional[Any]:
        """召回记忆"""

    def forget(self, key: str) -> None:
        """遗忘记忆"""

    def get_context_summary(self) -> str:
        """获取上下文摘要"""
```

### 2. 中期记忆 (cold.py)

```python
class ColdMemory:
    """中期记忆 - Cold Memory"""

    def __init__(self, retention_days: int = 30):
        self.retention_days = retention_days

    def store_fact(self, fact: str, category: str = "general") -> None:
        """存储事实（用 § 分隔）"""

    def store_preference(self, preference: str) -> None:
        """存储偏好"""

    def get_recent(self, days: int = 7) -> list[str]:
        """获取近期记忆"""

    def archive_old(self) -> None:
        """归档旧记忆"""
```

### 3. 归档记忆 (archive.py)

```python
class ArchiveMemory:
    """归档记忆 - Archive"""

    def archive(self, memory_id: str, memory_content: str) -> None:
        """归档记忆"""

    def restore(self, archive_id: str) -> str:
        """恢复归档"""

    def search_archive(self, query: str) -> list[dict]:
        """搜索归档"""
```

### 4. 记忆整合 (memory.py)

```python
class MemoryManager:
    """
    记忆管理器 - 参考 Hermes 设计

    核心职责：
    1. 管理 hot/cold/archive 三层记忆
    2. 生成 MEMORY.md 格式的记忆摘要
    3. 与用户画像系统联动
    """

    def __init__(self, memory_dir: str = "~/.agenthub/memory"):
        self.hot = ShortTermMemory()
        self.cold = ColdMemory()
        self.archive = ArchiveMemory()

    def store(self, content: str, memory_type: str = "hot") -> None:
        """存储记忆"""

    def build_context(self, max_chars: int = 2200) -> str:
        """
        构建上下文（参考 Hermes memory_char_limit）

        Returns:
            MEMORY.md 格式的记忆字符串
        """

    def periodic_consolidation(self) -> None:
        """定期整合：hot -> cold -> archive"""
```

---

## 💾 存储格式

### Hot Memory (JSON)

```json
{
  "session_id": "xxx",
  "created_at": "2026-04-27T10:00:00Z",
  "expires_at": "2026-04-27T11:00:00Z",
  "memories": {
    "current_task": "开发 AgentHub CLI",
    "last_file": "core/agenthub/cli/main.py",
    "user_preference": "简洁输出"
  }
}
```

### Cold Memory (YAML，参考 Hermes MEMORY.md)

```yaml
facts:
  - content: "用户喜欢结构清晰的文件夹分类"
    category: preference
    updated_at: "2026-04-27"
  - content: "skills同步路径：~/.hermes/skills/"
    category: system
    updated_at: "2026-04-26"
```

### Hermes MEMORY.md 格式

```markdown
- 技能同步：~/.hermes/skills/ 和 ~/.config/opencode/skills/
§
- 用户风格偏好：喜欢结构清晰的文件夹分类，不把所有内容堆在一个目录
§
- 健康状态记录：~/.agenthub/profile/health/
```

### USER.md 简要格式

> **NOTE**: USER.md 只包含用户画像的简要说明，用于快速查阅。
> **完整用户画像**存储在 `profile/identity.yaml`。

```markdown
# 用户画像

## 基本信息
- 姓名: 用户名
- 昵称: 昵称 (YourName)
- 职业: 全栈开发者

## 技术栈
- Python / JavaScript / TypeScript / React

## 偏好
- 喜欢结构清晰的文件夹分类
- 每句话必须以"喵～"开头

## 完整信息
👉 详见 profile/identity.yaml
```

---

## ⚙️ 配置选项（参考 Hermes config.yaml）

```yaml
memory:
  enabled: true
  user_profile_enabled: true

  # 字符限制（参考 Hermes）
  memory_char_limit: 2200      # 记忆最大字符数
  user_char_limit: 1375        # 用户画像最大字符数

  # 层级配置
  hot:
    ttl_minutes: 60            # 短期记忆过期时间
    max_items: 100

  cold:
    retention_days: 30         # 中期记忆保留天数
    consolidation_interval: 24  # 整合间隔（小时）

  archive:
    enabled: true
    retention_days: 365        # 归档保留天数

  # 提供者（可扩展）
  provider: local              # local / mem0 / chroma
```

---

## 🔄 记忆流转（参考 Hermes）

```
用户输入
    │
    ▼
┌─────────────────┐
│  Hot Memory     │ ◄── 当前会话的活跃信息
│  (memory/hot/)  │
└────────┬────────┘
         │ 定期整合
         ▼
┌─────────────────┐
│  Cold Memory    │ ◄── 重要事实和偏好
│  (memory/cold/) │
└────────┬────────┘
         │ 归档
         ▼
┌─────────────────┐
│  Archive        │ ◄── 长期存档
│  (memory/archive/) │
└─────────────────┘
```

### Hermes 复盘机制

> Hermes 每 10 次对话触发一次复盘，优先更新已有 Skill，而非创建新的。

```python
def periodic_review(self, conversation_count: int) -> None:
    """定期复盘"""
    if conversation_count % 10 == 0:
        self.consolidate_memories()
        self.update_memory_md()
```

---

## 🔗 与其他模块的关系

```
┌─────────────────────────────────────────────────┐
│                    AgentHub                       │
├─────────────────────────────────────────────────┤
│  ┌─────────┐   ┌─────────┐   ┌─────────────┐   │
│  │  Skill  │   │  Agent  │   │   Profile   │   │
│  └────┬────┘   └────┬────┘   └──────┬──────┘   │
│       │              │               │           │
│       └──────────────┼───────────────┘           │
│                      ▼                           │
│              ┌─────────────┐                     │
│              │   Memory    │                     │
│              │   System    │                     │
│              └─────────────┘                     │
│                      │                           │
│                      ▼                           │
│              ┌─────────────┐                     │
│              │ memories/   │                     │
│              │ MEMORY.md   │                     │
│              │ USER.md     │───路由到───▶ profile/
│              └─────────────┘                     │
└─────────────────────────────────────────────────┘
```

### 用户画像路由机制

```
┌──────────────────┐
│  memories/       │
│  USER.md        │  ◄── 简要说明（快速查阅）
│                  │
│  # 用户画像      │
│  ## 基本信息     │
│  姓名: xxx       │
│  ## 偏好         │
│  每句话以"喵～"开头│
│                  │
│  👉 详见 profile/ │
└────────┬─────────┘
         │ 路由
         ▼
┌──────────────────┐
│  profile/        │  ◄── 完整信息（权威来源）
│                  │
│  identity.yaml   │  ◄── 身份信息
│  skills.md       │  ◄── 技能图谱
│  projects.md     │  ◄── 项目经验
│  contacts/       │  ◄── 联系人
│  health/         │  ◄── 健康记录
│  growth/         │  ◄── 成长轨迹
│  learning/       │  ◄── 学习资料
└──────────────────┘
```

---

## 📊 对比：AgentHub vs Hermes

| 特性 | Hermes | AgentHub |
|------|--------|----------|
| 记忆存储 | 纯文件 | 文件 + SQLite |
| 用户画像 | USER.md（单一） | `profile/` 目录（完整结构） |
| 画像路由 | ❌ 无 | ✅ USER.md → profile/identity.yaml |
| 事实存储 | MEMORY.md | memory/memories/MEMORY.md |
| 分隔符 | `§` | `§` (兼容) |
| 层级 | hot/cold/archive | hot/cold/archive |
| 提供者 | mem0 | local (可扩展) |
| 跨平台 | 单机 | 跨工具同步 |

### AgentHub 用户画像优势

| 特性 | 说明 |
|------|------|
| **结构化存储** | 分离的身份、技能、偏好、联系人等 |
| **路由机制** | USER.md 简要 → profile/ 完整 |
| **工具无关** | YAML + Markdown，任何 AI 都能读取 |
| **跨平台共享** | 一次配置，多工具通用 |

---

## 🔐 隐私与安全

| 措施 | 说明 |
|------|------|
| **本地存储** | 记忆默认存储在本地 `~/.agenthub/memory/` |
| **选择性同步** | 用户可配置哪些记忆同步到云端 |
| **加密存储** | 敏感记忆可加密存储 |
| **清理机制** | 自动过期清理，长期未访问的记忆归档 |

---

*本文档参考 Hermes Agent 记忆系统设计，由 AgentHub 实现。*
