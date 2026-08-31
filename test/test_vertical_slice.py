import time
from pathlib import Path

from fastapi.testclient import TestClient

from agenthub.main import create_app


def test_vertical_slice_end_to_end(tmp_path: Path) -> None:
    app = create_app(
        database_url=f"sqlite:///{tmp_path / 'agenthub.db'}",
        artifact_root=str(tmp_path / "artifacts"),
    )
    client = TestClient(app)

    ws = client.post("/api/v1/workspaces", json={"name": "ws-1", "description": "demo"}).json()
    provider = client.post(
        "/api/v1/model-providers",
        json={"workspace_id": ws["id"], "name": "openai-compatible", "kind": "openai", "endpoint": "http://example"},
    ).json()
    tool = client.post(
        "/api/v1/mcp-servers",
        json={"workspace_id": ws["id"], "name": "github-mcp", "tool_type": "mcp_server", "endpoint": "http://mcp", "enabled": True},
    ).json()
    agent = client.post(
        "/api/v1/agents",
        json={
            "workspace_id": ws["id"],
            "name": "coding-agent",
            "model_provider_id": provider["id"],
            "instructions": ["Do work"],
            "capabilities": ["coding"],
            "tool_ids": [tool["id"]],
        },
    ).json()

    task = client.post(
        "/api/v1/tasks",
        json={
            "workspace_id": ws["id"],
            "requesting_agent": agent["id"],
            "assigned_agent": agent["id"],
            "objective": "analyze repository",
            "required_context": {"repo": "demo"},
            "permitted_tools": [tool["name"]],
            "constraints": {"budget": "low"},
            "expected_output_schema": {"type": "object"},
            "timeout_seconds": 60,
            "priority": 3,
            "trace_id": "trace-123",
            "depth": 1,
        },
    )
    assert task.status_code == 200

    run_id = task.json()["run_id"]
    for _ in range(20):
        run = client.get(f"/api/v1/runs/{run_id}").json()
        if run["status"] == "completed":
            break
        time.sleep(0.1)

    assert run["status"] == "completed"
    assert run["result"]["status"] == "success"

    events = client.get(f"/api/v1/runs/{run_id}/events").json()
    assert any(e["event_type"] == "run.queued" for e in events)
    assert any(e["event_type"] == "run.completed" for e in events)

    artifacts = client.get("/api/v1/artifacts", params={"run_id": run_id}).json()
    assert artifacts and Path(artifacts[0]["path"]).exists()

    audit_logs = client.get("/api/v1/audit-logs", params={"workspace_id": ws["id"]}).json()
    assert any(log["action"] == "task_submitted" for log in audit_logs)
