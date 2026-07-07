# AgentHub 部署流程

> 版本: v1.1 | 创建: 2026-04-28 | 更新: 2026-04-28

---

## 1. 概述

本文档记录 AgentHub 的部署和初始化流程。

---

## 2. 目录说明

### 2.1 正式使用必须保留

```
.agenthub/
├── agents/           # Agent 配置模板
├── apps/            # 应用程序（dashboard/landing-page/tool-detector）
├── docs/            # 文档
├── memory/          # 记忆系统数据
├── profile/         # 用户画像
├── projects/        # 项目文件
├── secrets/         # 密钥
├── skills/          # 共享 Skill 库
├── TODO/            # 待办事项
├── README.md        # 项目说明
├── registry.json    # 注册表
└── pyproject.toml   # Python 配置
```

### 2.2 已通过 .gitignore 排除

这些文件夹**不会被 git 提交**，仅本地使用：

| 文件夹/文件 | 说明 |
|-------------|------|
| `dev/` | 开发相关（临时脚本、测试文件） |
| `.obsidian/` | Obsidian 编辑器元数据 |
| `runtime/` | 运行时数据 |
| `.secrets/` | 密钥（实际存储在 secrets/） |

---

## 3. 开发规范

**临时文件和测试文件统一放到 `dev/` 目录**，这样不会被 git 提交。

```
.agenthub/dev/
├── test_skill.py    # 临时测试
├── 错误原因分析.md   # 临时笔记
└── ...
```

---

## 4. 密钥管理

`secrets/` 目录包含敏感信息：
- 不提交到 Git
- 使用 .gitignore 排除

---

## 5. 更新日志

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.1 | 2026-04-28 | 精简目录：删除 scripts/、test/、test_memory/、skills-library/ |
| v1.0 | 2026-04-28 | 初始版本 |

---

*本文档 v1.1 | AgentHub 部署流程*
