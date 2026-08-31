# Agent Hub Architecture (MVP)

This repository now includes a production-oriented **modular-monolith MVP** implementing:

- Workspace isolation
- Agent / Tool / Model registries
- Task + Run execution runtime
- Structured run events + SSE stream endpoint
- Artifact persistence
- Audit trail
- YAML workbench configuration schema validation

## Runtime Components

- **API runtime**: FastAPI (`core/agenthub/main.py`)
- **State store**: PostgreSQL (Compose) with SQL schema in `db/migrations/001_init.sql`
- **Queue/cache substrate**: Redis (Compose, reserved for async scaling)
- **Artifact store**: local path in MVP, MinIO provisioned in Compose

## Vertical Slice Implemented

1. Create workspace
2. Register model provider
3. Connect tool / MCP server
4. Create agent
5. Submit delegated task contract
6. Execute run (background task)
7. Stream/list execution events
8. Persist result artifact
9. Inspect run history and audit logs

## Security and Governance (MVP controls)

- Delegation depth limit (`depth <= 4`)
- Tool allow-list per task (`permitted_tools`)
- Explicit task contract fields including `trace_id`
- Immutable audit records per operation
- Artifact and run history retention in durable DB/file storage

## Extensibility Path

The following seams are explicitly prepared for extraction:

- Runtime executor (replace in-process worker with queue workers)
- Storage backends (S3 + object metadata abstraction)
- Provider adapters (OpenAI-compatible, Ollama, vLLM, custom HTTP)
- Policy engine (approval gates + RBAC + budget enforcement)
