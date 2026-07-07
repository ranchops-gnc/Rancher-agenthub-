# 目录结构说明

## 完整目录树

```
agent-system/
├── SPEC.md                    # 本规范文档
├── README.md                  # 总览文档
├── LICENSE                   # MIT License
│
├── profile/                   # 👤 用户画像（唯一真相来源）
│   ├── identity.md           # 基础身份信息
│   ├── skills.md            # 技能图谱
│   ├── projects.md          # 项目经验
│   ├── health/              # 健康记录
│   │   ├── body.md         # 身体健康
│   │   └── mental.md        # 心理健康
│   ├── growth/              # 成长轨迹
│   │   ├── plan.md         # 发展规划
│   │   └── history.md       # 成长历史
│   ├── learning/           # 学习记录
│   └── contacts/           # 联系人
│       ├── 冯雪薇/
│       ├── 罗婉然/
│       └── 黄海潼/
│
├── secrets/                   # 🔐 敏感信息（不提交Git）
│   └── .gitkeep             # 保持目录结构
│
├── skills/                    # 🛠️ 共享技能库
│   ├── README.md            # 技能索引
│   ├── system-core/        # 系统核心（必读）
│   ├── dev-agent/           # 开发Agent
│   ├── life-agent/          # 生活Agent
│   ├── ops-agent/           # 运营Agent
│   └── [专业技能]/          # 如 github, email, browser-bridge 等
│
├── agents/                    # 🤖 Agent配置
│   ├── README.md            # Agent索引
│   ├── router.md            # 路由规则
│   ├── main-agent.md        # 主Agent配置
│   ├── dev-agent.md         # 开发Agent
│   ├── life-agent.md        # 生活Agent
│   ├── ops-agent.md         # 运营Agent
│   └── productivity-agent.md # 效率Agent
│
├── projects/                  # 📁 项目配置
│   ├── README.md           # 项目索引
│   └── todo/              # 待办任务
│
└── docs/                     # 📚 文档指南
    ├── structure.md         # 目录结构说明
    ├── quick-start.md       # 快速开始
    ├── naming-convention.md # 命名规范
    └── task-handoff.md      # 任务交接规范
```

## 各目录说明

### profile/ - 用户画像

用户真实信息，是所有AI工具的**"真相来源"**。

| 文件/目录 | 说明 |
|-----------|------|
| `identity.md` | 姓名、联系方式、学校、专业等基础信息 |
| `skills.md` | 技术栈、已掌握技能、待学技能 |
| `projects.md` | 项目经历和作品 |
| `health/` | 健康记录（身体、心理） |
| `growth/` | 成长轨迹和规划 |
| `learning/` | 学习资料和笔记 |
| `contacts/` | 联系人信息 |

### secrets/ - 敏感信息

**重要**：此目录不提交GitHub，包含：
- 账号密码
- API Keys
- 私有密钥

### skills/ - 共享技能库

AI技能集合，每个技能包含：
- `SKILL.md` - 技能定义（必须）
- `references/` - 参考资料（可选）
- `scripts/` - 自动化脚本（可选）
- `templates/` - 模板文件（可选）

### agents/ - Agent配置

定义不同角色的AI Agent及其职责：

| Agent | 职责 | 触发词 |
|-------|------|--------|
| main-agent | 总调度、意图识别、路由分发 | 通用入口 |
| dev-agent | 开发任务 | 开发、代码、编程、网站、API |
| life-agent | 生活服务 | 日程、课程、作业、天气、情感 |
| ops-agent | 运营任务 | 博客、飞书、微信、邮件、PPT |
| productivity-agent | 效率工具 | 自动化、批量、脚本 |

### projects/ - 项目配置

具体项目的配置和待办事项：
- `todo/` - 任务看板
- 项目级配置变量

### docs/ - 文档指南

使用说明和文档：
- `structure.md` - 目录结构说明
- `quick-start.md` - 快速开始指南
- `naming-convention.md` - 命名规范
- `task-handoff.md` - 任务交接规范

---

*最后更新：2026-04-26*
