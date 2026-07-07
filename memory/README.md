# 记忆系统

> 版本: v2.0 | 更新: 2026-04-29

---

## 概述

AgentHub 记忆系统采用简化架构，参考 Hermes 设计，只保留实际使用的结构。

---

## 目录结构

```
memory/
├── core/                     # ★ 核心记忆（永久，AI 必读）
│   ├── MEMORY.md            #   重要事实（用 § 分隔）
│   └── USER.md              #   用户画像
├── session/                  # 会话记忆（运行时）
└── persist/                  # 持久化记忆（归档）
```

---

## 层级说明

| 层级 | TTL | 说明 |
|------|-----|------|
| core | 永久 | MEMORY.md + USER.md，AI 必读 |
| session | 会话级 | 当前会话的活跃信息 |
| persist | 永久 | 归档的记忆片段 |

---

## 快速开始

### 对话开始时
1. 读取 `memory/core/MEMORY.md`
2. 读取 `memory/core/USER.md`

### 对话中发现新信息
- 立即追加到 `memory/core/MEMORY.md`，用 `§` 分隔

### 遇到错误或踩坑
- 追加到 `memory/core/MEMORY.md`

---

## 详细规范

见 `memory/SKILL.md`

---

*AgentHub 记忆系统 v2.0 · 基于 Hermes 设计*