# AgentHub AI Developer Guide

> For AI agents: How to understand, use, and extend AgentHub

## Project Overview

AgentHub is an **AI Tools Management Platform** that provides:
- Centralized management of multiple AI tools (OpenClaw, Claude, Codex, etc.)
- Shared memory and profile system for multi-AI collaboration
- Skill registry for reusable capabilities
- Agent scheduling and task management

## Quick Setup

```bash
# Install in editable mode
pip install -e D:\code\github\agenthub

# Initialize user directories
agenthub init

# Verify installation
agenthub --help
```

## Architecture

### Dual Working Directory Design

```
~/.agenthub/           # AgentHub core (open source, no privacy data)
~/.xavier/            # User private data (shared across AI tools)
```

**Why two directories?**
- `~/.agenthub/` - Contains AgentHub's own configs, skills, agents (can be shared publicly)
- `~/.xavier/` - Contains user's private data: API keys, memory, profiles (shared by all AI tools)

### Source Code Structure

```
src/agenthub/
├── __init__.py
├── cli/                    # CLI entry point
│   ├── main.py            # Click CLI root
│   └── commands/          # Subcommands
│       ├── skill.py       # skill install/list/search/...
│       ├── agent.py       # agent list/status/...
│       ├── task.py       # task submit/list/...
│       └── registry.py   # registry management
└── core/                  # Core modules
    ├── skill/             # Skill system
    │   ├── loader.py      # Load SKILL.md
    │   ├── parser.py      # Parse skill metadata
    │   ├── registry.py    # Skill registry
    │   ├── dependency.py  # Dependency resolution
    │   └── sync.py        # Sync from shared-skills
    ├── agent/             # Agent system
    │   ├── router.py      # Route tasks to agents
    │   ├── scheduler.py   # Task scheduling
    │   ├── state.py       # Agent state
    │   ├── models.py      # Data models
    │   └── adapters/      # Agent adapters
    │       ├── base.py    # Base adapter
    │       ├── claude_adapter.py
    │       ├── opencode_adapter.py
    │       └── codex_adapter.py
    ├── memory/            # Memory system
    │   ├── levels.py      # L0-L4 memory levels
    │   ├── short_term.py  # Short-term memory
    │   ├── long_term.py   # Long-term memory
    │   ├── knowledge.py   # Knowledge graph
    │   ├── context.py     # Context extraction
    │   └── retrieval.py   # Memory retrieval
    └── database/          # Persistence
        └── manager.py     # SQLite manager
```

## Key Modules

### 1. Skill System (`core/skill/`)

**Purpose**: Manage reusable capability packages called "Skills"

**Workflow**:
1. `loader.py` reads `SKILL.md` in skill directory
2. `parser.py` extracts metadata (name, version, tags, triggers)
3. `registry.py` maintains installed skills index
4. `dependency.py` resolves skill dependencies
5. `sync.py` syncs skills from shared-skills directory

**Skill Format**:
```yaml
---
name: github-pr
version: 1.0.0
description: GitHub PR management tool
author: Xavier
tags: [github, pr, code-review]
triggers: [pr, pull request, github]
dependencies: []
---

# Skill content here
```

**Skill Directory**:
```
skills/
└── github-pr/
    ├── SKILL.md          # Required: skill definition
    ├── references/       # Optional: reference docs
    ├── templates/        # Optional: template files
    └── scripts/          # Optional: automation scripts
```

### 2. Agent System (`core/agent/`)

**Purpose**: Route tasks to appropriate AI agents

**Flow**:
```
User Task → Router → Scheduler → Adapter → External AI Tool
                     ↓
              State Manager
```

**Adapters**: Each AI tool (Claude, OpenCode, Codex) has an adapter that:
- Converts unified task format to tool-specific format
- Handles tool-specific authentication
- Parses tool-specific responses

### 3. Memory System (`core/memory/`)

**Purpose**: Multi-level memory management inspired by human memory

| Level | Name | TTL | Storage |
|-------|------|-----|---------|
| L0 | Instant | 5 min | Token cache |
| L1 | Working | 1 hour | Memory/file |
| L2 | Short-term | 7 days | File |
| L3 | Long-term | Permanent | File |
| L4 | Knowledge | Permanent | Graph DB |

**Usage**:
```python
from agenthub.core.memory import MemoryEngine

engine = MemoryEngine("~/.xavier/memory")
item = engine.add("User likes Python", level="L2", tags=["preference"])
results = engine.search("Python preferences")
```

## Multi-AI Collaboration

### Shared Resources

```
~/.xavier/
├── profile/           # User profiles (all AIs can read)
│   ├── personality.json
│   ├── preferences.json
│   └── habits.json
├── secrets/           # API keys (authorized AIs only)
│   ├── github.md
│   ├── openai.md
│   └── anthropic.md
└── memory/           # Long-term memory (all AIs can read/write)
    ├── short-term/
    ├── long-term/
    └── knowledge/
```

### How AIs Use Shared Resources

1. **Read user profile**: When starting, AI reads `~/.xavier/profile/` to understand user preferences
2. **Store memories**: After learning something important, AI saves to `~/.xavier/memory/`
3. **Query secrets**: When needing API keys, AI reads from `~/.xavier/secrets/` (if authorized)
4. **Cross-AI learning**: AI can query memories created by other AIs

## CLI Commands

```bash
agenthub skill list              # List installed skills
agenthub skill install <path>     # Install a skill
agenthub skill search <query>     # Search skills
agenthub skill info <name>       # Show skill details
agenthub skill uninstall <name>  # Uninstall a skill

agenthub agent list              # List available agents
agenthub agent status            # Show agent status

agenthub task submit "task" --agent claude  # Submit task
agenthub task list --status pending         # List tasks

agenthub registry info           # Show registry info
```

## Extending AgentHub

### Adding a New Skill

1. Create skill directory in `skills/`:
   ```
   skills/my-skill/
   ├── SKILL.md
   └── ...
   ```

2. Add to SKILL.md:
   ```yaml
   ---
   name: my-skill
   version: 1.0.0
   description: What this skill does
   triggers: [keyword1, keyword2]
   ---
   ```

3. Install: `agenthub skill install skills/my-skill`

### Adding a New Agent Adapter

1. Create adapter in `core/agent/adapters/`:
   ```python
   from .base import BaseAdapter

   class MyAdapter(BaseAdapter):
       def __init__(self):
           super().__init__("my-agent")

       def execute(self, task):
           # Implement agent-specific logic
           pass
   ```

2. Register in `core/agent/router.py`

### Adding CLI Commands

1. Add command in `cli/commands/`:
   ```python
   import click

   @click.command()
   @click.argument('name')
   def my_command(name):
       """My custom command"""
       click.echo(f"Hello {name}")
   ```

2. Register in `cli/__init__.py`

## Important Conventions

1. **No hardcoded paths**: Use `pathlib.Path` and environment variables
2. **JSON for data**: All shared data uses JSON format
3. **YAML for config**: Skills and agents use YAML metadata
4. **Type hints**: Use type hints for all function signatures
5. **Error handling**: Wrap external calls in try/except with clear messages

## Configuration

### pyproject.toml

```toml
[tool.setuptools.packages.find]
where = ["src"]  # Source code is in src/

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### Build and Install

```bash
# Development install
pip install -e .

# Build distribution
python -m build

# Install from distribution
pip install dist/agenthub-*.whl
```

## Troubleshooting

**CLI not found after install**:
```bash
python -m agenthub.cli.main --help
```

**Import errors**:
```bash
# Verify src/ is in Python path
python -c "import sys; print(sys.path)"
# Should include the agenthub package location
```

**Skill not loading**:
```bash
# Check registry
agenthub registry info
# Verify skill directory has SKILL.md
```

## File Locations

| Item | Path |
|------|------|
| Project root | `D:\code\github\agenthub` |
| Source code | `D:\code\github\agenthub\src\agenthub` |
| Skills library | `D:\code\github\agenthub\skills` |
| Agent configs | `D:\code\github\agenthub\agents` |
| Docs | `D:\code\github\agenthub\docs` |
| Tests | `D:\code\github\agenthub\tests` |

## Development Notes

- User private data goes in `~/.xavier/` (not in project repo)
- API keys/secrets should never be committed
- Use `~/.agenthub/shared/` for cross-AI resources
- All Chinese comments should be translated to English before committing

---

*For questions about specific modules, read the module's `__init__.py` for documentation.*
