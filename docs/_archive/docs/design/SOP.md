# AgentHub SOP - 项目初始化标准流程

> 本文档定义其他 AI 工具接入 AgentHub 的标准化流程。
> 所有 AI 工具应按此 SOP 执行初始化和任务交付。

---

## 📋 SOP 概览

```
┌─────────────────────────────────────────────────────────────┐
│                    AgentHub SOP 流程                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣ 环境检测   →   2️⃣ 安装依赖   →   3️⃣ 初始化项目          │
│        ↓                                    ↓               │
│  4️⃣ 加载核心模块                      5️⃣ 验证安装          │
│        ↓                                    ↓               │
│  6️⃣ 开始工作   ←   8️⃣ 任务交付   ←   7️⃣ 执行任务          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 第一步：环境检测

### 检查项

| 检查项 | 命令 | 预期结果 |
|--------|------|----------|
| Python 版本 | `python --version` | ≥ 3.10 |
| Git | `git --version` | 任意版本 |
| 项目路径 | `ls agenthub/` | 项目文件存在 |
| pip | `pip --version` | 可用 |

### 执行脚本

```bash
# 检测 Python 版本
python --version

# 检测项目是否存在
if [ ! -d "D:/code/github/agenthub" ]; then
    echo "❌ 项目不存在，请先 clone"
    exit 1
fi

# 进入项目目录
cd D:/code/github/agenthub
echo "✅ 项目目录: $(pwd)"
```

---

## 第二步：安装依赖

### 自动安装（推荐）

```powershell
# PowerShell - 自动化安装
cd D:\code\github\agenthub

# 安装核心依赖
pip install -e .

# 安装 Web 依赖
cd web/backend
pip install -r requirements.txt

echo "✅ 依赖安装完成"
```

### 手动检查清单

```bash
# 检查已安装的包
pip list | grep -E "click|rich|pyyaml|semver|fastapi|uvicorn"

# 如缺少，手动安装
pip install click>=8.0 rich>=13.0 pyyaml>=6.0 semver>=3.0
pip install fastapi>=0.100 uvicorn pydantic
```

---

## 第三步：初始化项目

### 初始化命令

```powershell
# 方式一：使用 CLI
cd D:\code\github\agenthub
agenthub init

# 方式二：手动初始化
$home = $env:USERPROFILE
New-Item -Path "$home\.agenthub\skills" -ItemType Directory -Force
New-Item -Path "$home\.agenthub\logs" -ItemType Directory -Force

Write-Host "✅ AgentHub 初始化完成"
Write-Host "   配置文件: $home\.agenthub\config.yaml"
Write-Host "   Skills目录: $home\.agenthub\skills"
```

### 初始化验证

```powershell
# 验证目录结构
Test-Path "$home\.agenthub\skills"  # 应返回 True
Test-Path "$home\.agenthub\logs"    # 应返回 True
Test-Path "$home\.agenthub\agenthub.db"  # 数据库文件（运行后生成）
```

---

## 第四步：加载核心模块

### Python 模块路径配置

```python
# -*- coding: utf-8 -*-
"""
AgentHub 快速初始化 - 其他 AI 工具使用
"""

import sys
from pathlib import Path

# ===== 项目路径配置 =====
PROJECT_ROOT = Path("D:/code/github/agenthub")
SRC_ROOT = PROJECT_ROOT / "src"

# 添加到 Python 路径
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

# ===== 核心模块导入 =====
try:
    from agenthub.core.skill.registry import SkillRegistry
    from agenthub.core.agent.scheduler import TaskScheduler
    from agenthub.core.agent.router import AgentRouter
    from agenthub.core.database import DatabaseManager
    
    # 全局实例
    registry = SkillRegistry()      # Skill 注册表
    db = DatabaseManager()          # 数据库
    router = AgentRouter()          # Agent 路由
    scheduler = TaskScheduler(router)  # 任务调度器
    
    print("✅ 核心模块加载成功")
    print(f"   - registry: {len(registry.list_all())} skills")
    print(f"   - router: {len(router._adapters)} agents")
    print(f"   - db: {db.db_path}")
    
except ImportError as e:
    print(f"⚠️ 核心模块导入失败: {e}")
    print("   尝试使用模拟模式...")
```

### 短期记忆配置

```python
# 其他 AI 工具应记住以下关键信息：
SHORT_TERM_MEMORY = {
    "project_root": "D:/code/github/agenthub",
    "skills_dir": "~/.agenthub/skills",
    "db_path": "~/.agenthub/agenthub.db",
    "api_port": 5173,
    "web_frontend": "D:/code/github/agenthub/web/frontend/index.html",
}
```

---

## 第五步：验证安装

### 快速验证命令

```powershell
# CLI 验证
cd D:\code\github\agenthub
python -c "
import sys
sys.path.insert(0, 'D:/code/github/agenthub/src')
from agenthub.core.skill.registry import SkillRegistry
r = SkillRegistry()
print(f'✅ Registry OK - {len(r.list_all())} skills')
"

# Web 验证（可选）
cd D:\code\github\agenthub\web\backend
python -c "
import uvicorn
from main import app
print('✅ FastAPI app OK')
"
```

### 验证检查清单

| 检查项 | 命令 | 预期 |
|--------|------|------|
| CLI 可用 | `agenthub --version` | 显示版本 |
| Skill 注册表 | `agenthub skill list` | 显示列表 |
| 数据库 | `Test-Path ~/.agenthub/agenthub.db` | True |
| Web API | 访问 localhost:5173 | JSON 响应 |

---

## 第六步：执行任务

### 标准任务流程

```python
# 1. 接收任务
task_prompt = "审查代码质量"

# 2. 查找匹配的 Skill
matched_skills = registry.find_by_trigger(task_prompt)
if matched_skills:
    skill = matched_skills[0]
    print(f"使用 Skill: {skill.name}")

# 3. 路由到 Agent
from agenthub.core.agent.models import Task
task = Task(
    name="代码审查",
    prompt=task_prompt,
    priority=TaskPriority.NORMAL
)

# 4. 提交执行
result = scheduler.submit(task)
if result.scheduled:
    print(f"✅ 任务已提交: {result.task_id}")
    # 等待完成
    task_result = scheduler.execute_next()
else:
    print(f"❌ 任务提交失败: {result.error}")
```

### 任务完成后

```python
# 保存结果到数据库
if task_result:
    db.save_execution(task.id, result.agent_name, task_result)
    print(f"✅ 执行完成: {task_result.result[:100]}...")
```

---

## 常用命令速查

### CLI 命令

```powershell
# 初始化
agenthub init

# Skills
agenthub skill list                    # 列出
agenthub skill install <path>          # 安装
agenthub skill uninstall <name>        # 卸载
agenthub skill search <query>          # 搜索
agenthub skill info <name>             # 详情

# Agents
agenthub agent list                    # 列出
agenthub agent status                  # 状态

# Tasks
agenthub task list                    # 列表
agenthub task submit "prompt"          # 提交
agenthub task cancel <id>              # 取消

# Registry
agenthub registry info                 # 信息
agenthub registry rebuild             # 重建
```

### Web UI

```powershell
# 启动后端
cd D:\code\github\agenthub\web\backend
python main.py
# 访问 http://localhost:5173

# 或直接打开前端（无后端模式）
start D:\code\github\agenthub\web\frontend\index.html
```

---

## 错误排查

| 错误 | 原因 | 解决 |
|------|------|------|
| `ModuleNotFoundError: agenthub` | 未安装 | `pip install -e .` |
| `PermissionError` | 权限不足 | 使用管理员运行 |
| `RegistryError` | 注册表损坏 | `agenthub registry rebuild` |
| Port 5173 被占用 | 端口冲突 | `netstat -ano \| findstr 5173` |

---

## 快速启动脚本

保存为 `scripts/quick-start.ps1`：

```powershell
# AgentHub 快速启动脚本
$ErrorActionPreference = "Stop"

Write-Host "🚀 AgentHub 快速启动" -ForegroundColor Cyan

# 1. 安装依赖
Write-Host "`n📦 安装依赖..." -ForegroundColor Yellow
cd D:\code\github\agenthub
pip install -e . --quiet
pip install fastapi uvicorn pydantic --quiet

# 2. 初始化
Write-Host "`n⚙️  初始化..." -ForegroundColor Yellow
$home = $env:USERPROFILE
New-Item -Path "$home\.agenthub\skills" -ItemType Directory -Force | Out-Null
New-Item -Path "$home\.agenthub\logs" -ItemType Directory -Force | Out-Null

# 3. 验证
Write-Host "`n✅ 验证安装..." -ForegroundColor Yellow
python -c "
import sys
sys.path.insert(0, 'D:/code/github/agenthub/src')
from agenthub.core.skill.registry import SkillRegistry
r = SkillRegistry()
print(f'   Registry: {len(r.list_all())} skills loaded')
"

Write-Host "`n🎉 AgentHub 就绪!" -ForegroundColor Green
Write-Host "   CLI: agenthub --help"
Write-Host "   Web: 打开 web/frontend/index.html"
```

---

## 其他 AI 工具接入指南

### 给子 Agent 的上下文

```
你是 AgentHub 项目的使用者。

项目路径: D:/code/github/agenthub
核心模块: src/agenthub/core/
CLI: agenthub 命令

初始化流程:
1. pip install -e D:/code/github/agenthub
2. agenthub init
3. python -c "from agenthub.core.skill.registry import SkillRegistry; ..."
```

### 短期记忆模板

```
[AgentHub Context - 短期记忆]
- project_root: D:/code/github/agenthub
- src_root: D:/code/github/agenthub/src
- skills_dir: ~/.agenthub/skills
- db_path: ~/.agenthub/agenthub.db
- web_port: 5173
- cli_entry: agenthub

初始化命令:
  pip install -e D:/code/github/agenthub
  agenthub init

核心模块导入:
  import sys
  sys.path.insert(0, 'D:/code/github/agenthub/src')
  from agenthub.core.skill.registry import SkillRegistry
```

---

*本文档版本: 1.0 | 更新: 2026-04-26*
