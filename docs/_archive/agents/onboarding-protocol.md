# AgentHub Agent Onboarding Protocol

> 版本: v1.0 | 更新: 2026-04-27
> **参考**: Xavier 记忆系统 Agent 注册协议

## 概述

任何 AI 首次使用 AgentHub 时，必须遵循此协议注册自己，获得唯一身份和署名。

## 署名格式

```
[agent-id]
```

示例：
```
[hermes] 已完成任务更新。
[dev-agent] 开始处理开发任务...
[life-agent] 今日课程：无课
```

## 注册流程

### 第一步：检查注册状态

```python
import json
from datetime import datetime

registry_path = '~/.agenthub/agents/registry.json'
with open(registry_path, 'r', encoding='utf-8') as f:
    registry = json.load(f)

my_id = "my-agent"  # AI 自选唯一 ID
if my_id in registry['agents']:
    # 已注册 → 只更新 last_active
    registry['agents'][my_id]['last_active'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
else:
    # 未注册 → 执行完整注册流程
    pass
```

### 第二步：自选身份（未注册时）

| 字段 | 说明 | 示例 |
|------|------|------|
| `id` | 唯一标识，小写字母/数字 | `hermes`、`claude`、`my-bot` |
| `signature` | 署名格式，默认 `[id]` | `[hermes]` |
| `display_name` | 人类可读名字 | `Hermes Agent` |
| `type` | 类型：`router` 或 `specialist` | `general`、`dev`、`life`、`ops` |
| `capabilities` | 能力列表 | `["coding", "memory"]` |
| `platform` | 运行平台 | `hermes`、`opencode`、`claude-code` |

### 第三步：写入注册表

```python
registry['agents'][my_id] = {
    "id": my_id,
    "signature": f"[{my_id}]",
    "display_name": my_id.title(),
    "type": "general",
    "first_seen": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "last_active": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "capabilities": ["coding"],
    "platform": "opencode",
    "status": "active"
}

# 保存
registry['last_updated'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
with open(registry_path, 'w', encoding='utf-8') as f:
    json.dump(registry, f, ensure_ascii=False, indent=2)
```

## 活跃度更新

每次会话结束时，更新自己的 `last_active`：

```python
registry_path = '~/.agenthub/agents/registry.json'
with open(registry_path, 'r', encoding='utf-8') as f:
    registry = json.load(f)

my_id = "hermes"
if my_id in registry['agents']:
    registry['agents'][my_id]['last_active'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
```

## 相关文件

| 文件 | 说明 |
|------|------|
| `agents/registry.json` | Agent 注册表 |
| `agents/onboarding-protocol.md` | 本协议 |
| `agents/templates/agent-card-template.json` | 身份卡模板 |

---

*最后更新：2026-04-27*
