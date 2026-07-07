# AgentHub 多级记忆系统设计

> 版本: v1.0 | 更新: 2026-04-26

## 概述

AgentHub 采用五级记忆体系，模拟人类记忆的层级结构，实现智能的记忆管理。

## 记忆分级

| 级别 | 名称 | 生命周期 | 存储方式 | 触发条件 |
|------|------|----------|----------|----------|
| **L0** | 瞬时记忆 | 5 分钟 | Token 缓存 | 每次交互 |
| **L1** | 工作记忆 | 1 小时 | 内存/文件 | 显式 @记住 |
| **L2** | 短期记忆 | 7 天 | 文件 | 多次提及/重要事件 |
| **L3** | 长期记忆 | 永久 | 文件 | 反复验证/用户确认 |
| **L4** | 知识图谱 | 永久 | 图数据库 | 实体关系 |

## 目录结构

```
~/.agenthub/memory/
├── L0_instant/          # 瞬时记忆
│   └── *.json
├── L1_working/          # 工作记忆
│   └── *.json
├── L2_short_term/      # 短期记忆
│   └── *.json
├── L3_long_term/       # 长期记忆
│   └── *.json
├── L4_knowledge/       # 知识图谱
│   ├── nodes/          # 实体节点
│   └── edges/         # 关系边
└── _index/            # 索引
    └── memory_index.json
```

## 核心模块

### levels.py - 记忆分级引擎

```python
from agenthub.core.memory import MemoryLevel, MemoryItem, MemoryEngine

# 创建记忆引擎
engine = MemoryEngine("~/.agenthub/memory")

# 添加记忆
item = engine.add(
    content="用户叫用户名",
    level=MemoryLevel.L2_SHORT_TERM,
    tags=["用户信息"],
    importance=0.8,
)

# 搜索记忆
results = engine.search("用户名", level=MemoryLevel.L2_SHORT_TERM)

# 升级记忆
engine.upgrade(item.id)  # 自动判断目标级别

# 清理过期记忆
cleaned = engine.cleanup()
```

### short_term.py - 短期记忆管理

```python
from agenthub.core.memory import ShortTermMemory, SessionMemory

# 创建短期记忆管理器
short_term = ShortTermMemory()

# 创建/加载会话
session = short_term.create_session("session_123")

# 添加对话轮次
short_term.add_turn("user", "我叫用户名")
short_term.add_turn("assistant", "好的，用户名")

# 提取关键事实
short_term.extract_to_working("用户名字：用户名")

# 列出所有会话
sessions = short_term.list_sessions()
```

### long_term.py - 长期记忆管理

```python
from agenthub.core.memory import LongTermMemory, EntityMemory

# 创建长期记忆管理器
long_term = LongTermMemory()

# 创建实体
entity = long_term.create_entity(
    entity_type="person",
    name="用户名",
    description="广州科技职业技术大学学生",
)

# 添加事实
long_term.add_fact_to_entity(
    entity.entity_id,
    fact="空中乘务专业",
    source="conversation",
    confidence=0.9,
)

# 添加关联
entity.add_relationship(
    related_to="AgentHub",
    rel_type="works_on",
    strength=0.8,
)

# 搜索实体
results = long_term.search("用户名")
```

### knowledge.py - 知识图谱

```python
from agenthub.core.memory import KnowledgeGraph, KGNode, KGEdge

# 创建知识图谱
kg = KnowledgeGraph()

# 添加节点
user_node = kg.add_node(
    label="用户名",
    node_type="person",
    properties={"role": "开发者"},
)

project_node = kg.add_node(
    label="AgentHub",
    node_type="project",
)

# 添加边
kg.add_edge(
    source_id=user_node.id,
    target_id=project_node.id,
    relation="WORKS_ON",
    weight=1.0,
)

# 获取邻居
neighbors = kg.get_neighbors(user_node.id)

# 图遍历
visited = kg.traverse(user_node.id, max_depth=2)
```

### context.py - 上下文提取器

```python
from agenthub.core.memory import ContextExtractor

# 创建提取器
extractor = ContextExtractor(short_term, long_term)

# 处理对话
info = extractor.process_conversation(
    role="user",
    content="我叫用户名，是广州科技职业技术大学的学生",
)

# 批量处理
conversations = [
    {"role": "user", "content": "我叫用户名"},
    {"role": "assistant", "content": "好的，用户名"},
    {"role": "user", "content": "我在做 AgentHub 项目"},
]
all_info = extractor.bulk_extract(conversations)
```

### retrieval.py - 记忆检索器

```python
from agenthub.core.memory import MemoryRetrieval

# 创建检索器
retrieval = MemoryRetrieval(engine, long_term, kg)

# 检索记忆
results = retrieval.retrieve("用户名", limit=10)

# 生成上下文字符串
context = retrieval.retrieve_with_context("用户名")
```

## 记忆流转

### 晋升路径

```
L0 (瞬时) → L1 (工作) → L2 (短期) → L3 (长期) → L4 (知识图谱)
```

**晋升条件：**
- L0 → L1：显式 @记住
- L1 → L2：同一信息被提及 3+ 次
- L2 → L3：信息被验证 5+ 次或用户确认
- L3 → L4：实体关系被明确建立

### 降级/遗忘路径

```
L2 (过期) → L1 (过期) → L0 (过期) → 清理
```

**降级条件：**
- 时间超过 TTL
- 重要性评分下降
- 用户明确遗忘

## 自动清理

```bash
# 清理过期记忆（建议每天执行）
agenthub memory cleanup

# 清理指定天数前的会话
agenthub memory cleanup --days 7
```

## CLI 命令

```bash
# 添加记忆
agenthub memory add "用户叫用户名" --level L2 --tags user_info

# 搜索记忆
agenthub memory search "用户名"

# 查看统计
agenthub memory stats

# 清理过期记忆
agenthub memory cleanup

# 导出记忆
agenthub memory export --format json
```

---

*本文档由 AgentHub 自动生成*
