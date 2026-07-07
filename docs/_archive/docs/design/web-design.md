# Web 管理界面设计

> AgentHub Web 端设计方案

## 页面结构

```
/
├── 仪表盘 (Dashboard)
│   ├── 系统状态概览
│   ├── 工具运行状态
│   ├── 最近活动
│   └── 快捷操作
│
├── 工具管理 (Tools)
│   ├── 工具列表
│   ├── 安装/卸载
│   ├── 配置编辑器
│   └── 启动/停止
│
├── 技能库 (Skills)
│   ├── 技能商店
│   ├── 已安装技能
│   ├── 技能详情
│   └── 技能市场
│
├── 网关管理 (Gateways)
│   ├── 网关列表
│   ├── 接入配置
│   ├── 消息日志
│   └── 连接状态
│
├── 部署中心 (Deploy)
│   ├── 部署任务
│   ├── 部署历史
│   └── 部署配置
│
└── 设置 (Settings)
    ├── 全局配置
    ├── 主题设置
    ├── 账号管理
    └── 关于
```

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端框架 | React / Vue 3 | SPA 应用 |
| UI 组件 | TailwindCSS / shadcn/ui | 现代化 UI |
| 状态管理 | Zustand / Pinia | 全局状态 |
| 后端框架 | FastAPI / Express | REST API |
| 数据库 | SQLite / PostgreSQL | 数据存储 |
| 实时通信 | WebSocket / SSE | 实时更新 |
| 认证 | JWT / Session | 用户认证 |

## API 设计

### 工具管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `GET /api/tools` | GET | 获取工具列表 |
| `GET /api/tools/:id` | GET | 获取工具详情 |
| `POST /api/tools/:id/start` | POST | 启动工具 |
| `POST /api/tools/:id/stop` | POST | 停止工具 |
| `DELETE /api/tools/:id` | DELETE | 卸载工具 |

### Skill 管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `GET /api/skills` | GET | 获取技能列表 |
| `GET /api/skills/:id` | GET | 获取技能详情 |
| `POST /api/skills/install` | POST | 安装技能 |
| `DELETE /api/skills/:id` | DELETE | 卸载技能 |

### 网关管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `GET /api/gateways` | GET | 获取网关列表 |
| `POST /api/gateways` | POST | 添加网关 |
| `GET /api/gateways/:id/status` | GET | 获取状态 |
| `POST /api/gateways/:id/start` | POST | 启动网关 |
| `POST /api/gateways/:id/stop` | POST | 停止网关 |

### 部署

| 接口 | 方法 | 说明 |
|------|------|------|
| `GET /api/deployments` | GET | 获取部署列表 |
| `POST /api/deploy` | POST | 创建部署 |
| `GET /api/deploy/:id/logs` | GET | 获取日志 |

## 数据模型

### Tool

```typescript
interface Tool {
  id: string;
  name: string;
  type: 'opencode' | 'openclaw' | 'codebuddy' | 'claude' | 'cursor' | 'hermes';
  status: 'running' | 'stopped' | 'error';
  config_path: string;
  version: string;
  installed_at: string;
  last_run: string;
}
```

### Skill

```typescript
interface Skill {
  id: string;
  name: string;
  description: string;
  category: string;
  author: string;
  version: string;
  installed: boolean;
  config: Record<string, any>;
}
```

### Gateway

```typescript
interface Gateway {
  id: string;
  type: 'wechat' | 'qq' | 'feishu' | 'telegram' | 'discord';
  name: string;
  status: 'connected' | 'disconnected' | 'error';
  config: Record<string, any>;
  messages_today: number;
  last_message: string;
}
```

---

*最后更新：2026-04-26*
