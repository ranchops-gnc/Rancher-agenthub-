# AgentHub 工作文件夹架构设计

> 版本: v1.0 | 更新: 2026-04-26

## 核心理念

AgentHub 的工作文件夹不仅服务于自身，还可以作为其他 AI 工具的**同级工作目录**，实现：
- 多 AI 工具共享用户数据
- 统一的记忆系统
- 集中化的用户画像和密钥管理

## 双工作文件夹设计

```
~/.agenthub/          # AgentHub 核心目录（开源，不含隐私）
~/.xavier/            # 用户私有数据（可被各 AI 共用）
```

### 各 AI 工具的工作文件夹

| AI 工具 | 主工作目录 | 私有数据目录 |
|---------|-----------|-------------|
| **AgentHub** | `~/.agenthub/` | `~/.xavier/` |
| **OpenClaw** | `~/.config/opencode/` | `~/.xavier/` |
| **WorkBuddy** | `~/.workbuddy/` | `~/.xavier/` |
| **Xavier** | `~/.xavier/` | - |

## 目录结构

### ~/.agenthub/ - AgentHub 核心

```
~/.agenthub/
├── config.json              # 主配置
├── skills/                  # 已安装 Skills
├── agents/                  # Agent 配置
├── memory/                  # 记忆系统
│   ├── L0_instant/         # 瞬时记忆 (5分钟)
│   ├── L1_working/         # 工作记忆 (1小时)
│   ├── L2_short_term/      # 短期记忆 (7天)
│   ├── L3_long_term/       # 长期记忆 (永久)
│   ├── L4_knowledge/       # 知识图谱
│   └── _index/             # 索引
├── shared/                  # ⭐ 共享资源（其他 AI 可用）
│   ├── memory/             # 共享记忆接口
│   ├── profile/            # 共享画像
│   └── knowledge/          # 共享知识库
├── data/                    # 数据存储
├── backup/                  # 备份
└── logs/                    # 日志
```

### ~/.xavier/ - 用户私有数据

```
~/.xavier/
├── memory/                  # 记忆系统
│   ├── short-term/         # 短期记忆 (L0/L1/L2)
│   ├── long-term/          # 长期记忆 (L3)
│   └── knowledge/          # 知识库 (L4)
├── profile/                 # 用户画像
│   ├── 性格.json
│   ├── 偏好.json
│   └── 习惯.json
├── secrets/                 # API 密钥
│   ├── github.md
│   ├── openai.md
│   └── anthropic.md
├── skills/                  # 私有 Skills
├── agents/                  # 私有 Agent 配置
├── 文档/                    # 个人文档
└── 项目/                    # 项目文件
```

## 共享资源协议

### 1. 记忆系统共享

其他 AI 工具可以通过标准接口访问 AgentHub 的记忆：

```
~/.agenthub/shared/memory/
├── sessions/              # 会话历史
├── facts/                # 事实库
└── context/             # 上下文
```

### 2. 用户画像共享

```
~/.xavier/profile/
├── basic.json           # 基本信息
├── preferences.json     # 偏好设置
├── habits.json          # 使用习惯
└── context.json         # 当前上下文
```

### 3. 知识库共享

```
~/.xavier/memory/knowledge/
├── nodes/               # 实体节点
├── edges/               # 关系边
└── documents/          # 文档
```

## AI 工具协作模式

### 模式 A：AgentHub 作为中枢

```
┌─────────────────────────────────────────────────────┐
│                  ~/.xavier/                        │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│   │ Profile │  │ Memory  │  │ Secrets │           │
│   └────┬────┘  └────┬────┘  └────┬────┘           │
│        │            │            │                 │
└────────┼────────────┼────────────┼─────────────────┘
         │            │            │
    ┌────┴────────────┴────────────┴────┐
    │           AgentHub               │
    │      ~/.agenthub/shared/         │
    └────────────────┬──────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───┴───┐      ┌────┴────┐      ┌────┴────┐
│OpenClaw│      │WorkBuddy│      │ Xavier  │
│        │      │         │      │         │
└─────────┘      └─────────┘      └─────────┘
```

### 模式 B：共享 Skills 和 Agents

```
~/.agenthub/shared/
├── skills/              # 各 AI 共用 Skills
│   ├── github-pr/
│   ├── email-sender/
│   └── document-gen/
├── agents/              # 各 AI 共用 Agent 配置
│   ├── developer/
│   └── researcher/
└── prompts/            # 共用提示词模板
    ├── code-review/
    └── research/
```

## 数据隔离策略

| 数据类型 | 存储位置 | 可见性 |
|---------|---------|--------|
| 用户画像 | `~/.xavier/profile/` | 所有 AI 可读 |
| API 密钥 | `~/.xavier/secrets/` | 仅授权 AI 可读 |
| 短期记忆 | `~/.xavier/memory/short-term/` | 创建者 AI 独占 |
| 长期记忆 | `~/.xavier/memory/long-term/` | 所有 AI 可读写 |
| 知识图谱 | `~/.xavier/memory/knowledge/` | 所有 AI 可读写 |
| AgentHub 配置 | `~/.agenthub/` | 仅 AgentHub |

## 实现要求

### 1. 标准数据格式

所有共享数据使用 JSON 格式：

```json
// ~/.xavier/profile/basic.json
{
  "name": "用户名",
  "language": "中文",
  "timezone": "Asia/Shanghai",
  "updated_at": "2026-04-26T12:00:00Z"
}
```

### 2. 访问控制

```python
# secrets 目录权限检查
def read_secret(ai_tool: str, key_name: str) -> str:
    """仅授权的 AI 工具可以读取密钥"""
    authorized = get_authorized_tools(key_name)
    if ai_tool not in authorized:
        raise PermissionError(f"{ai_tool} 未授权读取 {key_name}")
    return read_file(f"~/.xavier/secrets/{key_name}")
```

### 3. 记忆同步

```python
# 各 AI 写入记忆的标准接口
def save_shared_memory(ai_tool: str, memory_type: str, data: dict):
    """保存共享记忆"""
    path = f"~/.agenthub/shared/memory/{ai_tool}/{memory_type}"
    write_json(path, data)

def query_shared_memory(query: str, limit: int = 10):
    """查询共享记忆"""
    return search_in_directory("~/.agenthub/shared/memory/", query, limit)
```

## 向后兼容

- AgentHub 现有 `~/.agenthub/` 结构保持不变
- 新增 `~/.xavier/` 作为用户私有数据目录
- `~/.agenthub/shared/` 作为 AI 间共享的标准接口

---

*本文档由 AgentHub 自动生成*
