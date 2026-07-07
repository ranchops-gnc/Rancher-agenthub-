# AgentHub

Cross-AI control plane for shared Skills, Agents, user profiles, memory, tools, MCP servers, runs, artifacts, and audit logs.

AgentHub is designed to make AI tools clients of one governed runtime instead of isolated systems that each own their own context.

## MVP Scope

This repository bootstraps a runnable vertical slice:

- Workspace creation
- Model provider registration
- Tool and MCP server registration
- Agent creation
- Task submission and run execution
- Run event querying and SSE streaming
- Artifact persistence
- Audit log querying
- YAML configuration validation with JSON Schema

## Core Modules

| Module | Purpose |
|---|---|
| Skill Registry | Versioned reusable skills using YAML frontmatter plus Markdown |
| Agent Registry | Router and specialist agent definitions with skill bindings |
| Profile System | Portable user identity and preferences |
| Memory System | Core, session, and persistent memory with scoped access |
| Tool Gateway | Capability-based tool and MCP authorization |
| Run Engine | Durable task execution, events, artifacts, and audit trail |
| Context Engine | Builds standardized context packages for agents |

## Architecture

See [`docs/architecture.md`](docs/architecture.md).

## API

See [`docs/api.md`](docs/api.md).

## Local Development

```bash
cp .env.example .env
docker compose up --build
```

API:

```bash
curl http://localhost:8080/health
```

## Privacy

This repository is a public open-source template. Do not commit private user data, secrets, tokens, or production memory exports.

## License

MIT
