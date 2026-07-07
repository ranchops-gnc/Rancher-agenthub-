---
name: agent
description: AgentHub 多级记忆系统，支持 L0-L4 五级记忆存储和检索，自动索引 ~/.agenthub 文件夹
license: MIT
triggers:
  []
metadata:
  version: "1.0.0"
  category: system
---

# AgentHub Agent 技能

> 多级记忆系统 - L0-L4 五级记忆体系

## 目录结构

```
~/.agenthub/memory/
├── short-term/              # 短期记忆
│   ├── L0/                # 瞬时记忆 (TTL=5分钟)
│   ├── L1/                # 工作记忆 (TTL=1小时)
│   └── L2/                # 短期记忆 (TTL=7天)
├── long-term/              # 长期记忆
│   └── entities/         # 实体存储
├── knowledge/             # 知识图谱
│   ├── nodes/            # 节点
│   └── edges/            # 边
└── _index/               # 索引文件
```

## 记忆级别

| 级别 | 名称 | TTL | 说明 |
|------|------|-----|------|
| L0 | 瞬时记忆 | 5分钟 | 单次对话中的临时信息 |
| L1 | 工作记忆 | 1小时 | 当前会话内重要的上下文 |
| L2 | 短期记忆 | 7天 | 跨会话的重要信息 |
| L3 | 长期记忆 | 永久 | 经反复验证的重要事实 |
| L4 | 知识图谱 | 永久 | 实体关系网络 |

## 使用方式

### Python API

```python
from agenthub.core.memory import create_memory

mem = create_memory()

# 记住内容
mem.remember("用户叫 用户名", level=2)

# 回忆内容
results = mem.recall("用户")

# 搜索记忆
results = mem.search("AgentHub")

# 获取统计
stats = mem.get_stats()
```

### 触发词

| 触发词 | 记忆级别 | 示例 |
|--------|----------|------|
| 普通提及 | L2 | "我的项目叫 AgentHub" |
| 记住 | L2 | "记住：项目名叫 AgentHub" |
| 重要 | L3 | "重要：这是API密钥" |
| 关系 | L4 | "用户和项目的关系是：创建者" |

## 自动索引

AgentHub 会自动索引 `~/.agenthub` 文件夹中的文件。

## 与其他 AI 工具共享

可通过符号链接或配置指向其他 AI 工具的记忆目录实现共享。

---

*最后更新：2026-04-26*
