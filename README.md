**AgentHub**
A Unified Shared Ecosystem for AI Tools across Four Pillars: Skills, Agents, User Profiles, and Memory Systems

License: MIT

---

🎯 **What is AgentHub?**
AgentHub is a cross-platform AI tool management system designed to solve the following challenges:

| Problem | Solution |
| --- | --- |
| AI tool configurations scattered across multiple places | Centralized configuration management |
| Reconfiguring settings every time a new tool is adopted | One-click deployment script |
| Lack of interoperability between different AI tools | Unified gateway access |
| Difficulty sharing and reusing Skill libraries | Centralized Skill resource repository |

---

✨ **Four Core Modules**

**1️⃣ Skill Library — Write Once, Run Anywhere**

| Feature | Description |
| --- | --- |
| Unified Format | YAML frontmatter + Markdown, vendor-agnostic |
| Cross-Platform Compatibility | Universal support for OpenClaw / OpenCode / Claude Code |
| Dependency Management | SemVer version control with automatic dependency resolution |
| Trigger Words | Intelligent user input matching with automatic Skill loading |

```
skills/
├── github-pr/              # GitHub PR management
├── browser-bridge/         # Browser automation
└── 50+ shared Skills

```

**2️⃣ Agent System — Specialized Roles, Intelligent Routing**

| Feature | Description |
| --- | --- |
| Type Definitions | Router + Specialist |
| Skill Binding | Automatic loading of required Skills |
| Memory Configuration | Customizable short-term/long-term memory strategies |

```
agents/
├── main-agent/             # Main routing entry point
├── dev-agent/              # Development specialist
├── life-agent/             # Life services
└── productivity-agent/     # Productivity tools

```

**3️⃣ User Profile — Tool-Agnostic, Permanently Portable**

| Feature | Description |
| --- | --- |
| Unified Format | YAML + Markdown, plain text and tool-agnostic |
| Identity Information | Basic details, contact info, social accounts |
| Preferences | Aesthetic tastes, communication styles, response habits |

```
profile/
├── identity.yaml           # Identity information
├── skills.md              # Skill map
└── contacts/              # Contacts

```

**4️⃣ Memory System — Persistent Memory, Continuous Learning**

| Feature | Description |
| --- | --- |
| Simplified Design | Three-tier structure: core + session + persist (inspired by Hermes) |
| Core Memory | `MEMORY.md` + `USER.md`, retained permanently |
| Session Memory | Runtime memory, archived periodically |

```
memory/
├── core/                   # Core memory (permanent)
│   ├── MEMORY.md          #   Key facts (delimited by §)
│   └── USER.md            #   User profile
├── session/                # Session memory (runtime)
└── persist/                # Persistent memory (archived)

```

---

🚀 **Quick Start**

**One-Click Installation (Recommended)**

```bash
curl -fsSL https://raw.githubusercontent.com/xuanyuanluoxue/AgentHub/main/misc/install.sh -o /tmp/install.sh && bash /tmp/install.sh

```

After running, select an option from the menu:

| Option | Description |
| --- | --- |
| 1 | Install AgentHub |
| 2 | Update AgentHub |
| 3 | Reinstall |
| 4 | Uninstall AgentHub |
| 5 | Open configuration directory |
| 6 | Exit |

**Installation Location**

* `~/.agenthub/` (Linux / macOS / WSL)

After installation, run `agenthub --help` to view help options.

---

🤖 **AI Integration Guide**

Copy and paste the following prompt to your AI:

> Please read `~/.agenthub/AGENTS.md` first to understand the AgentHub integration guidelines.

Alternatively, instruct the AI to execute the following steps:

1. Read `~/.agenthub/AGENTS.md` — AI User Guide
2. Read `~/.agenthub/agents/registry.json` — Check registration status
3. Read `~/.agenthub/memory/core/MEMORY.md` — Load core memory
4. Read `~/.agenthub/profile/identity.yaml` — Get user details

---

📁 **Directory Structure**

```
~/.agenthub/
├── AGENTS.md              # ★ AI User Guide
├── README.md              # This file
│
├── skills/                # Skill library
│   ├── 00-SKILL-SPEC.md  #   Skill authoring specification
│   └── {skill}/          #   Individual Skill directories
│
├── agents/                # Agent configurations
│   ├── registry.json      #   Agent registry
│   ├── router.md          #   Routing rules
│   └── {type}-agent.md   #   Individual Agent configurations
│
├── memory/                # Memory system
│   ├── core/              #   Core memory
│   ├── session/          #   Session memory
│   └── persist/          #   Persistent memory
│
├── profile/               # User profile
│   ├── identity.yaml      #   Identity information
│   └── contacts/          #   Contacts
│
├── TODO/                  # Task tracking
│   ├── 00-TODO-SPEC.md   #   TODO specification
│   └── README.md          #   Usage instructions
│
├── secrets/               # Sensitive credentials (excluded from Git)
└── docs/                  # Design documentation

```

---

📚 **Documentation Navigation**

| Document | Description |
| --- | --- |
| `AGENTS.md` | ★ Essential for AI — Core guide for AI usage |
| `skills/00-SKILL-SPEC.md` | Skill authoring specification |
| `memory/SKILL.md` | Memory system documentation |
| `TODO/00-TODO-SPEC.md` | TODO task tracking specification |

---

⚠️ **Privacy Notice**
AgentHub is a public, open-source template project that contains no personal data.

* All paths, accounts, and names used in the documentation serve strictly as placeholders.
* To use this repository, please create your own configuration based on the provided template.

---

📄 **License**
MIT License

*Vision-driven, code-implemented.*
