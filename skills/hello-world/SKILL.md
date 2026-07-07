---
name: hello-world
description: Hello World 示例 Skill，演示 Skill 基本结构
license: MIT
triggers:
  []
metadata:
  version: "1.0.0"
  category: productivity
---

# Hello World Skill

这是一个示例 Skill，用于演示 AgentHub Skill 的标准格式。

## 功能

- 展示 Skill 的基本结构
- 提供触发词匹配示例
- 演示如何编写 Skill 文档

## 使用方法

当你说 "hello" 或 "你好" 时，这个 Skill 会被触发。

## 目录结构

```
hello-world/
├── SKILL.md         # 核心定义（必需）
├── README.md        # 详细文档（可选）
├── scripts/         # 脚本目录
│   └── greet.py    # 问候脚本
└── assets/         # 资源目录
    └── greeting.txt
```

## 触发词

- `hello` - 英文问候
- `你好` - 中文问候

## 进阶

查看 AgentHub 文档了解如何编写自己的 Skill：
- `skills/00-SKILL-SPEC.md` - Skill 格式规范
