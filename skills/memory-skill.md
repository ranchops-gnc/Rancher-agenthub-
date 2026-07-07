# 记忆系统

> 版本: v2.0 | 更新: 2026-04-29 | 基于 Hermes 简化设计

---

## 1. 目录结构

```
memory/
├── core/                     # ★ 核心记忆（永久）
│   ├── MEMORY.md            #   重要事实（用 § 分隔）
│   └── USER.md              #   用户画像
├── session/                  # 会话记忆（运行时内存）
└── persist/                  # 持久化记忆（归档）
```

**简化说明**：
- 移除 `hot/cold/archive` 三级分层，改为 `session/` + `persist/`
- 移除 `_index/`、`knowledge/`、`retrieval/` 过度设计
- 参考 Hermes，只保留实际使用的结构

---

## 2. 记忆层级

| 层级 | TTL | 说明 |
|------|-----|------|
| core | 永久 | MEMORY.md + USER.md，AI 必读 |
| session | 会话级 | 运行时内存，会话结束可选择持久化 |
| persist | 永久 | 归档的记忆片段 |

---

## 3. 核心文件

### 3.1 MEMORY.md

```markdown
# MEMORY.md

> 重要事实与偏好记录，使用 `§` 分隔不同条目

## 格式说明

每条记忆使用 `§` 分隔：
```
- 事实/偏好内容1
§
- 事实/偏好内容2
```

## 记忆条目

- 事实/偏好内容1
§
- 事实/偏好内容2
§
- 踩坑记录：xxx
```

**规则**:
- 用 `§` 作为分隔符，独占一行
- 不要覆盖已有内容，只做追加
- AI 输出可选带署名：`[agent-id]`

### 3.2 USER.md

```markdown
# USER.md

## 基本信息
- 姓名：xxx
- 角色：xxx
- 偏好：xxx

## 联系人
- xxx：xxx
```

---

## 4. 读写规范

### 4.1 对话开始时读取

```
1. 读取 core/MEMORY.md 了解重要事实
2. 读取 core/USER.md 了解用户画像
```

### 4.2 对话中写入

```
✅ 发现新信息 → 追加到 core/MEMORY.md（使用 § 分隔）
✅ 完成复杂任务 → 可选择写入 persist/
✅ 遇到错误/踩坑 → 追加到 core/MEMORY.md
```

### 4.3 归档流转

```
session/ → persist/
    │          │
 会话结束     永久
```

---

## 5. AI 使用规范

| 时机 | 操作 | 路径 |
|------|------|------|
| 对话开始 | 读取核心记忆 | `memory/core/MEMORY.md` + `USER.md` |
| 发现新信息 | 追加到核心记忆 | `memory/core/MEMORY.md` |
| 完成复杂任务 | 可选持久化 | `memory/persist/` |
| 遇到错误 | 追加到核心记忆 | `memory/core/MEMORY.md` |

---

## 6. 标签说明

| 标签 | 说明 |
|------|------|
| `skill` | 技能相关 |
| `preference` | 用户偏好 |
| `project` | 项目信息 |
| `system` | 系统配置 |
| `workflow` | 工作流程 |

---

*AgentHub 记忆系统 v2.0 · 简化自 Hermes 设计*