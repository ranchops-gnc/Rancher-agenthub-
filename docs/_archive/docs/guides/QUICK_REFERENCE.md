# AgentHub Quick Reference

## Common Tasks

### Install and Setup
```bash
pip install -e D:\code\github\agenthub
agenthub init
```

### Work with Skills
```bash
agenthub skill list                    # List all skills
agenthub skill install /path/to/skill  # Install skill
agenthub skill search github           # Search skills
agenthub skill info github-pr          # Skill details
agenthub skill uninstall github-pr     # Remove skill
```

### Work with Agents
```bash
agenthub agent list     # List available agents
agenthub agent status   # Show agent status
```

### Memory Operations
```python
from agenthub.core.memory import MemoryEngine

engine = MemoryEngine("~/.xavier/memory")

# Save memory
engine.add("User prefers dark mode", level="L2", tags=["preference"])

# Search memory
results = engine.search("dark mode")

# Get recent
recent = engine.get_recent(level="L2", limit=10)
```

### Access User Profile
```python
import json
from pathlib import Path

profile_dir = Path.home() / ".xavier" / "profile"
if profile_dir.exists():
    prefs = json.loads((profile_dir / "preferences.json").read_text())
```

### Access Secrets
```python
from pathlib import Path

secrets_dir = Path.home() / ".xavier" / "secrets"
if (secrets_dir / "github.md").exists():
    github_key = (secrets_dir / "github.md").read_text()
```

## Directory Reference

```
~/.agenthub/           # AgentHub core config
├── skills/           # Installed skills
├── agents/          # Agent configs
├── memory/          # AgentHub's own memory
└── shared/          # Shared resources

~/.xavier/           # User private data (shared across AIs)
├── profile/         # User preferences
├── secrets/         # API keys
├── memory/         # Long-term memory
│   ├── short-term/ # L0-L2 memories
│   ├── long-term/  # L3 memories
│   └── knowledge/  # L4 knowledge graph
├── skills/         # User's private skills
└── agents/         # User's agent configs
```

## Source Code Imports

```python
# CLI
from agenthub.cli.main import cli

# Core modules
from agenthub.core.skill.loader import SkillLoader
from agenthub.core.skill.registry import SkillRegistry
from agenthub.core.agent.router import AgentRouter
from agenthub.core.agent.scheduler import TaskScheduler
from agenthub.core.memory import MemoryEngine, MemoryLevel
from agenthub.core.database import DatabaseManager

# Adapters
from agenthub.core.agent.adapters import ClaudeAdapter, OpenCodeAdapter, CodexAdapter
```

## Skill Format

```yaml
# SKILL.md
---
name: skill-name
version: 1.0.0
description: What this skill does
author: YourName
tags: [tag1, tag2]
triggers: [trigger1, trigger2]
dependencies: []
---

Skill content in Markdown...
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AGENTHUB_HOME` | Override `~/.agenthub` location |
| `XAVIER_HOME` | Override `~/.xavier` location |
| `GH_TOKEN` | GitHub personal access token |

## Status Codes

| Status | Meaning |
|--------|--------|
| `pending` | Task waiting to be processed |
| `running` | Task currently executing |
| `completed` | Task finished successfully |
| `failed` | Task failed |
| `cancelled` | Task was cancelled |
