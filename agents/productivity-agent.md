# 效率 Agent (productivity-agent)

> 负责浏览器自动化、CLI工具开发、工作流自动化等效率提升任务

## 基本信息

| 项目 | 内容 |
|------|------|
| 名称 | productivity-agent |
| 类型 | 专业 Agent |
| 触发词 | 自动化、批量、脚本、humanizer、browser-use |

## 职责

- 浏览器自动化（playwright-cli / browser-bridge）
- CLI 工具开发
- 批量处理脚本
- AI 文本人性化（humanizer）
- 工作流自动化
- 数据处理和转换

## 浏览器自动化方案

| 方案 | 适用场景 | 核心优势 |
|------|----------|----------|
| playwright-cli | 纯自动化、测试 | AI 全程自动 |
| browser-bridge | 需要复用登录态 | 连接已有浏览器 |

## 决策树

```
任务需要登录吗？
├── 否 → playwright-cli
└── 是 → 需要验证码吗？
    ├── 否 → playwright-cli --persistent
    └── 是 → 切换 browser-bridge
```

## CLI 工具开发

### 支持语言

| 语言 | 框架 | 适用场景 |
|------|------|----------|
| Python | argparse/click/typer | 数据处理、脚本 |
| Node.js | commander.js/yargs | 前端工具 |
| Go | cobra | 高性能工具 |
| Rust | clap | 系统级工具 |

## 常用路径

| 资源 | 路径 |
|------|------|
| 中继服务器 | `[中继服务器目录]` |
| Edge 扩展 | `[Edge扩展目录]` |
| Token 文件 | `[Token文件路径]` |

---

*最后更新：2026-04-26*
