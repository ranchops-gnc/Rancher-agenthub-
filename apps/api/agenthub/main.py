from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI(title="AgentHub", version="0.1.0")


class WorkspaceCreate(BaseModel):
    name: str
    description: str | None = None


class ProviderCreate(BaseModel):
    name: str
    provider_type: str = Field(alias="type")
    config: dict[str, Any] = Field(default_factory=dict)


class ToolCreate(BaseModel):
    name: str
    tool_type: str = Field(alias="type")
    capabilities: list[str] = Field(default_factory=list)
    config: dict[str, Any] = Field(default_factory=dict)


class AgentCreate(BaseModel):
    name: str
    agent_type: str = Field(alias="type")
    instruction: str
    skills: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)


class RunCreate(BaseModel):
    agent_id: str | None = None
    input: dict[str, Any] = Field(default_factory=dict)


DB: dict[str, dict[str, Any]] = {
    "workspaces": {},
    "providers": {},
    "tools": {},
    "agents": {},
    "runs": {},
    "events": {},
    "artifacts": {},
    "audit": {},
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_id() -> str:
    return str(uuid.uuid4())


def audit(workspace_id: str, actor: str, action: str, target: str | None, payload: dict[str, Any]) -> None:
    event_id = make_id()
    DB["audit"][event_id] = {
        "id": event_id,
        "workspace_id": workspace_id,
        "actor": actor,
        "action": action,
        "target": target,
        "payload": payload,
        "created_at": now(),
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "agenthub-api", "environment": os.getenv("AGENTHUB_ENV", "development")}


@app.post("/workspaces")
def create_workspace(payload: WorkspaceCreate) -> dict[str, Any]:
    workspace_id = make_id()
    item = {"id": workspace_id, **payload.model_dump(), "created_at": now()}
    DB["workspaces"][workspace_id] = item
    audit(workspace_id, "system", "workspace.created", workspace_id, item)
    return item


@app.get("/workspaces/{workspace_id}")
def get_workspace(workspace_id: str) -> dict[str, Any]:
    return DB["workspaces"][workspace_id]


@app.post("/workspaces/{workspace_id}/providers")
def create_provider(workspace_id: str, payload: ProviderCreate) -> dict[str, Any]:
    provider_id = make_id()
    item = {"id": provider_id, "workspace_id": workspace_id, **payload.model_dump(by_alias=False), "created_at": now()}
    DB["providers"][provider_id] = item
    audit(workspace_id, "system", "provider.created", provider_id, item)
    return item


@app.get("/workspaces/{workspace_id}/providers")
def list_providers(workspace_id: str) -> list[dict[str, Any]]:
    return [p for p in DB["providers"].values() if p["workspace_id"] == workspace_id]


@app.post("/workspaces/{workspace_id}/tools")
def create_tool(workspace_id: str, payload: ToolCreate) -> dict[str, Any]:
    tool_id = make_id()
    item = {"id": tool_id, "workspace_id": workspace_id, **payload.model_dump(by_alias=False), "created_at": now()}
    DB["tools"][tool_id] = item
    audit(workspace_id, "system", "tool.created", tool_id, item)
    return item


@app.get("/workspaces/{workspace_id}/tools")
def list_tools(workspace_id: str) -> list[dict[str, Any]]:
    return [t for t in DB["tools"].values() if t["workspace_id"] == workspace_id]


@app.post("/workspaces/{workspace_id}/agents")
def create_agent(workspace_id: str, payload: AgentCreate) -> dict[str, Any]:
    agent_id = make_id()
    item = {"id": agent_id, "workspace_id": workspace_id, **payload.model_dump(by_alias=False), "created_at": now()}
    DB["agents"][agent_id] = item
    audit(workspace_id, "system", "agent.created", agent_id, item)
    return item


@app.get("/workspaces/{workspace_id}/agents")
def list_agents(workspace_id: str) -> list[dict[str, Any]]:
    return [a for a in DB["agents"].values() if a["workspace_id"] == workspace_id]


@app.post("/workspaces/{workspace_id}/runs")
def create_run(workspace_id: str, payload: RunCreate) -> dict[str, Any]:
    run_id = make_id()
    item = {"id": run_id, "workspace_id": workspace_id, "agent_id": payload.agent_id, "status": "completed", "input": payload.input, "output": {"message": "MVP run completed. Replace this with durable execution."}, "created_at": now(), "updated_at": now()}
    DB["runs"][run_id] = item
    DB["events"][run_id] = [
        {"id": make_id(), "run_id": run_id, "event_type": "run.started", "payload": {}, "created_at": now()},
        {"id": make_id(), "run_id": run_id, "event_type": "run.completed", "payload": item["output"], "created_at": now()},
    ]
    audit(workspace_id, "system", "run.completed", run_id, item)
    return item


@app.get("/workspaces/{workspace_id}/runs/{run_id}")
def get_run(workspace_id: str, run_id: str) -> dict[str, Any]:
    run = DB["runs"][run_id]
    assert run["workspace_id"] == workspace_id
    return run


@app.get("/workspaces/{workspace_id}/runs/{run_id}/events")
def list_run_events(workspace_id: str, run_id: str) -> list[dict[str, Any]]:
    run = DB["runs"][run_id]
    assert run["workspace_id"] == workspace_id
    return DB["events"].get(run_id, [])


@app.get("/workspaces/{workspace_id}/runs/{run_id}/events/stream")
def stream_run_events(workspace_id: str, run_id: str) -> StreamingResponse:
    events = list_run_events(workspace_id, run_id)

    async def generate():
        for event in events:
            yield f"event: {event['event_type']}\ndata: {event}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/workspaces/{workspace_id}/runs/{run_id}/artifacts")
def list_artifacts(workspace_id: str, run_id: str) -> list[dict[str, Any]]:
    run = DB["runs"][run_id]
    assert run["workspace_id"] == workspace_id
    return [a for a in DB["artifacts"].values() if a["run_id"] == run_id]


@app.get("/workspaces/{workspace_id}/audit")
def list_audit(workspace_id: str) -> list[dict[str, Any]]:
    return [a for a in DB["audit"].values() if a["workspace_id"] == workspace_id]
