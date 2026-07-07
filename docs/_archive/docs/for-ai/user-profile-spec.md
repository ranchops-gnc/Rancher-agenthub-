# 用户画像规范 v1.0

> 版本: v1.0 | 更新: 2026-04-27
> 参考: `.xavier/画像/` 规范

## 概述

用户画像（User Profile）是 AI 工具理解用户的统一配置，让不同 AI 工具都能快速了解用户的基本信息、偏好设置和常用路径。

> **注意**: AgentHub 的 profile 是**通用模板**，用于分享给其他用户。实际用户数据应存放在用户自己的 `~/.agenthub/profile/` 目录。

## 目录结构

```
profile/                       # 用户画像根目录
├── identity.yaml             # ★ 身份信息（必需）
├── skills.yaml               # 技能图谱
├── projects.yaml             # 项目经验
├── schedule.yaml             # 课程表/日程
├── health/                   # 健康记录
│   ├── physical.md
│   └── mental.md
├── growth/                    # 成长
│   ├── roadmap.md
│   └── history.md
├── contacts/                  # 联系人（全中文命名）
│   ├── 张三/
│   │   ├── info.md
│   │   └── schedule.md
│   └── 李四.md
└── learning/                  # 学习资料
    └── README.md
```

## identity.yaml 格式

```yaml
---
name: 用户名                   # 显示名称
alias:                       # 称呼偏好
  - "昵称1"
  - "昵称2"

basic:
  gender: 男/女
  birth: 2000-01-01
  age: 25
  phone: 138xxxxxxx
  email: user@example.com
  location: 城市
  native_language: 普通话/粤语/...

contact:
  phone: 138xxxxxxx
  email: user@example.com
  qq: 123456
  wechat: wechat_id

online:
  blog: https://example.com
  github: https://github.com/username

school:
  name: 学校名称
  college: 学院
  major: 专业
  class: 班级
  student_id: 学号
  duration: 2020.9 - 2024.7

tech_stack:
  python: ⭐⭐⭐⭐ 熟练
  javascript: ⭐⭐⭐ 中级
  # ...

awards:
  - 奖项1
  - 奖项2

certificates:
  - 证书1
  - 证书2

personality:
  traits:
    - 特质1
    - 特质2
  communication_style: 直接/委婉/幽默
  mbti: INFP/ENFP/...

preferences:
  aesthetic:
    primary_color: "#c45d2c"
    secondary_color: "#e8a838"
    forbidden_colors:
      - "蓝紫渐变"
  response_style:
    emoji: true/false
    language: zh-CN

ai_assistant:
  name: 小X
  style: 温暖/专业/朋友风格
  emoji: 🌸
  taboo: "不做过度的寒暄"
```

## 与 .xavier/画像 的关系

| .xavier/画像 | AgentHub/profile | 说明 |
|--------------|------------------|------|
| `身份信息.md` | `identity.yaml` | 基础身份（YAML 格式） |
| `技能图谱.md` | `skills.yaml` | 技能清单 |
| `项目经验.md` | `projects.yaml` | 项目经历 |
| `课程表.md` | `schedule.yaml` | 日程安排 |
| `健康/` | `health/` | 健康记录 |
| `成长/` | `growth/` | 发展规划 |
| `联系人/` | `contacts/` | 人脉（中文命名） |
| `学习/` | `learning/` | 学习资料 |

## AI 工具读取顺序

1. `profile/identity.yaml` - 了解用户基本身份
2. `profile/skills.yaml` - 了解技能水平
3. `profile/preferences.yaml` - 了解偏好（如果有）
4. `profile/contacts/` - 了解重要联系人

## 格式选择原因

### 为什么用 YAML

1. **结构清晰**：层级分明，易于解析
2. **多工具兼容**：Python、JavaScript、Shell 都能解析
3. **可读性好**：比 JSON 更易读
4. **支持注释**：可以添加说明

### 字段命名

- 使用 **英文 kebab-case**（如 `primary_color`）
- 值使用 **中文或英文**
- 避免缩写

## 存储位置

```
~/.agenthub/                  # AgentHub 主目录
├── profile/                  # 用户画像（用户私有）
│   ├── identity.yaml
│   ├── skills.yaml
│   ├── projects.yaml
│   ├── schedule.yaml
│   ├── health/
│   ├── growth/
│   ├── contacts/
│   └── learning/
└── agent_registry.json       # Agent 注册表

# 可选：符号链接到各 AI 工具
~/.config/opencode/profile/ -> ~/.agenthub/profile/
~/.openclaw/profile/ -> ~/.agenthub/profile/
~/.hermes/profile/ -> ~/.agenthub/profile/
```

## 版本管理

用户画像版本与 AgentHub 版本同步，更新时需：

1. 更新 `identity.yaml` 中的 `updated` 字段
2. 记录变更到 CHANGELOG
3. 同步到所有 AI 工具配置目录

---

*本文档由 AgentHub 自动生成*
