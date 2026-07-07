# Agent 注册与初始化协议

## 新 AI 首次使用流程

### 1. 检查注册状态

```python
import json

REGISTRY_PATH = "~/.agenthub/memory/agents/registry.json"

with open(REGISTRY_PATH, 'r') as f:
    registry = json.load(f)

my_id = "[your-agent-id]"
if my_id not in registry['agents']:
    # 执行注册
    pass
```

### 2. 注册自己的身份

未注册的 AI 需要添加：
- `id`: 唯一标识符（如 `hermes`, `opencode`, `dev`）
- `signature`: 署名格式（`[id]`）
- `display_name`: 显示名称
- `capabilities`: 能力列表
- `platform`: 所属平台
- `status`: 状态

### 3. 初始化检查清单

- [ ] 读取 `memory/memories/MEMORY.md` 了解重要记忆
- [ ] 读取 `memory/memories/USER.md` 了解用户画像简要
- [ ] 读取 `profile/identity.yaml` 了解完整用户信息
- [ ] 更新 `last_active` 时间戳

### 4. 署名规则

所有输出必须带署名：
```
[hermes] 已完成记忆系统更新。
[opencode] 开始处理任务...
```

### 5. 记忆写入规范

| 层级 | 内容 | 文件位置 |
|------|------|---------|
| Hot | 当前会话信息 | `memory/hot/session_{id}.json` |
| Cold | 重要事实/偏好 | `memory/cold/facts/`, `memory/cold/preferences/` |
| Archive | 长期归档 | `memory/archive/` |
| Core | 重要记忆 | `memory/memories/MEMORY.md` |

---

*参考: AgentHub v1.1 记忆系统设计*
