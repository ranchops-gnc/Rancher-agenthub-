# Agent Hub API (MVP)

## Core endpoints

- `POST /api/v1/workspaces`
- `POST /api/v1/model-providers`
- `POST /api/v1/tools`
- `POST /api/v1/mcp-servers`
- `GET /api/v1/mcp-servers?workspace_id=...`
- `POST /api/v1/agents`
- `POST /api/v1/tasks`
- `GET /api/v1/runs?workspace_id=...`
- `GET /api/v1/runs/{run_id}`
- `GET /api/v1/runs/{run_id}/events`
- `GET /api/v1/runs/{run_id}/events/stream`
- `GET /api/v1/artifacts?run_id=...`
- `GET /api/v1/audit-logs?workspace_id=...`
- `GET /health`

Run the server:

```bash
agenthub serve
```

OpenAPI:

- `http://localhost:8000/docs`
- `http://localhost:8000/openapi.json`
