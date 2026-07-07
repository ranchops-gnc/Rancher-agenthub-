# Agent 路由规则

## 路由表

| 关键词 | Agent | 说明 |
|--------|-------|------|
| 开发、代码、编程、网站、API | dev-agent | 全栈开发、Android |
| Android、Kotlin、小程序 | dev-agent | 移动开发 |
| 日程、课程表、作业、天气 | life-agent | 生活服务 |
| 情感、恋爱、脱单、简历 | life-agent | 情感咨询 |
| 博客、文章、部署 | ops-agent | 内容运营 |
| 飞书、微信、邮件、文档、PPT | ops-agent | 运营工具 |
| 自动化、批量、脚本 | productivity-agent | 效率工具 |
| humanizer、AI痕迹 | productivity-agent | 文本处理 |

## 路由决策树

```
用户输入
    │
    ├── 开发类 → dev-agent
    │      └── 关键词: 开发、代码、编程、网站、API
    │                 Android、小程序、Git
    │
    ├── 生活类 → life-agent
    │      └── 关键词: 日程、课程、作业、天气
    │                 情感、简历、待办
    │
    ├── 运营类 → ops-agent
    │      └── 关键词: 博客、飞书、微信、邮件
    │                 文档、PPT、二维码
    │
    └── 效率类 → productivity-agent
           └── 关键词: 自动化、批量、脚本
                      humanizer、browser-use
```

## Skill 查找优先级

1. `skills/` - AgentHub 共享 Skill 库
2. 项目自定义 Skill 目录

## Agent 间通信

### 共享上下文
- 交接文档: `projects/templates/task.md`
- 共享技能: `skills/`

### 任务交接格式
交接文档存放于 `projects/templates/task.md`

## 约束规则

1. **不喧宾夺主** - 复杂任务必须路由到专业 Agent
2. **传递完整上下文** - 在 prompt 中包含用户需求和相关文件路径
3. **记录交接** - 复杂任务使用任务交接文档
4. **汇总结果** - 专业 Agent 完成后整合结果返回用户

---

*最后更新：2026-04-26*
