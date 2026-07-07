# AgentHub API

Base URL:

```text
http://localhost:8080
```

## Health

```http
GET /health
```

## Workspaces

```http
POST /workspaces
GET /workspaces/{workspace_id}
```

## Providers

```http
POST /workspaces/{workspace_id}/providers
GET /workspaces/{workspace_id}/providers
```

## Tools and MCP Servers

```http
POST /workspaces/{workspace_id}/tools
GET /workspaces/{workspace_id}/tools
```

## Agents

```http
POST /workspaces/{workspace_id}/agents
GET /workspaces/{workspace_id}/agents
```

## Runs

```http
POST /workspaces/{workspace_id}/runs
GET /workspaces/{workspace_id}/runs/{run_id}
GET /workspaces/{workspace_id}/runs/{run_id}/events
GET /workspaces/{workspace_id}/runs/{run_id}/events/stream
```

## Artifacts

```http
GET /workspaces/{workspace_id}/runs/{run_id}/artifacts
```

## Audit

```http
GET /workspaces/{workspace_id}/audit
```
