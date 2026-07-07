# Agent 配置

> ⚠️ **模板目录**: 本目录包含 Agent 配置模板，不包含任何私人信息。
> 所有路径和配置均为占位符，请基于此模板创建你自己的配置。

## Agent 类型

| Agent | 用途 | 类型 |
|-------|------|------|
| main-agent | 主 Agent（路由入口） | router |
| dev-agent | 开发任务 | specialist |
| life-agent | 生活服务 | specialist |
| ops-agent | 运营任务 | specialist |
| productivity-agent | 效率工具 | specialist |

## 配置说明

每个 Agent 配置包含：
- 角色定义（AGENT.md）
- 技能绑定（skills/）
- 记忆策略（memory/）

## Agent 规范

详见 `skills/00-SKILL-SPEC.md`（Skill 规范包含 Agent 相关约定）。

## 目录结构

```
agents/
├── README.md
├── main-agent.md           # 主路由 Agent
├── router.md               # 路由规则
├── dev-agent/              # 开发 Agent
│   └── AGENT.md
├── life-agent/             # 生活 Agent
│   └── AGENT.md
├── ops-agent/              # 运营 Agent
│   └── AGENT.md
└── productivity-agent/     # 效率 Agent
    └── AGENT.md
```
