# MEMORY.md

> 重要事实与偏好记录，使用 `§` 分隔不同条目

## 格式说明

每条记忆使用 `§` 分隔：
```
- 事实/偏好内容1
§
- 事实/偏好内容2
```

## 记忆条目示例（占位符）

```
- 项目结构：使用多Agent分工架构
§
- 项目架构：采用符号链接方案，各工具目录链接到 ~/.agenthub/
§
- 项目规范：skill 格式基于 YAML frontmatter + Markdown，支持跨工具共享
§
- 项目脚本：scripts/setup-symlinks.ps1 用于创建符号链接
§
- 共享范围：skills、agents、profile、memory、config
§

## AI 工具注册表
- 路径：`memory/core/ai-registry.json`
- 说明：各 AI 工具在此注册自己的配置位置和功能清单，AgentHub 通过此注册表自动发现并接入新工具

## 注册表结构
```json
{
  "tools": {
    "tool-name": {
      "name": "显示名称",
      "config_path": "配置目录路径",
      "skills_path": "技能库路径（可选）",
      "capabilities": {
        "subagents": ["子Agent列表"],
        "memory_system": true,
        "skills": true,
        "gateway": true,
        "channels": ["支持的通道"]
      },
      "last_updated": "最后更新时间"
    }
  }
}
```
```

## 标签说明

| 标签 | 说明 |
|------|------|
| `skill` | 技能相关 |
| `preference` | 用户偏好 |
| `project` | 项目信息 |
| `system` | 系统配置 |
| `workflow` | 工作流程 |

---

*本文件由 AgentHub 记忆系统管理，请勿手动编辑重要内容*
