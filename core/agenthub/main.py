from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Workspace(Base):
    __tablename__ = "workspaces"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class ModelProvider(Base):
    __tablename__ = "model_providers"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    kind: Mapped[str] = mapped_column(String(60), nullable=False)
    endpoint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Tool(Base):
    __tablename__ = "tools"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    tool_type: Mapped[str] = mapped_column(String(60), nullable=False)
    endpoint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    enabled: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Agent(Base):
    __tablename__ = "agents"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_provider_id: Mapped[str] = mapped_column(ForeignKey("model_providers.id"), nullable=False)
    instructions: Mapped[list[str]] = mapped_column(JSON, default=list)
    capabilities: Mapped[list[str]] = mapped_column(JSON, default=list)
    tool_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    parent_task_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    requesting_agent: Mapped[str] = mapped_column(ForeignKey("agents.id"), nullable=False)
    assigned_agent: Mapped[str] = mapped_column(ForeignKey("agents.id"), nullable=False)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    required_context: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    permitted_tools: Mapped[list[str]] = mapped_column(JSON, default=list)
    constraints: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    expected_output_schema: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    timeout_seconds: Mapped[int] = mapped_column(Integer, default=300)
    priority: Mapped[int] = mapped_column(Integer, default=5)
    trace_id: Mapped[str] = mapped_column(String(64), nullable=False)
    depth: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="queued")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Run(Base):
    __tablename__ = "runs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    task_id: Mapped[str] = mapped_column(ForeignKey("tasks.id"), nullable=False, unique=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="queued")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class RunEvent(Base):
    __tablename__ = "run_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(60), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Artifact(Base):
    __tablename__ = "artifacts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id"), nullable=False)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    artifact_type: Mapped[str] = mapped_column(String(60), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    actor: Mapped[str] = mapped_column(String(120), nullable=False)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    target_type: Mapped[str] = mapped_column(String(60), nullable=False)
    target_id: Mapped[str] = mapped_column(String(36), nullable=False)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class WorkspaceCreate(BaseModel):
    name: str
    description: str | None = None


class ModelProviderCreate(BaseModel):
    workspace_id: str
    name: str
    kind: str
    endpoint: str | None = None


class ToolCreate(BaseModel):
    workspace_id: str
    name: str
    tool_type: str = Field(description="api|cli|mcp_server|internal")
    endpoint: str | None = None
    enabled: bool = True


class AgentCreate(BaseModel):
    workspace_id: str
    name: str
    description: str | None = None
    model_provider_id: str
    instructions: list[str] = Field(default_factory=list)
    capabilities: list[str] = Field(default_factory=list)
    tool_ids: list[str] = Field(default_factory=list)


class TaskCreate(BaseModel):
    parent_task_id: str | None = None
    workspace_id: str
    requesting_agent: str
    assigned_agent: str
    objective: str
    required_context: dict[str, Any] = Field(default_factory=dict)
    permitted_tools: list[str] = Field(default_factory=list)
    constraints: dict[str, Any] = Field(default_factory=dict)
    expected_output_schema: dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = 300
    priority: int = 5
    trace_id: str
    depth: int = 0


def _id() -> str:
    return str(uuid.uuid4())


def create_app(database_url: str = "sqlite:///./agenthub.db", artifact_root: str = "./artifacts") -> FastAPI:
    engine = create_engine(database_url, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)
    artifact_dir = Path(artifact_root)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    app = FastAPI(title="Agent Hub API", version="0.1.0")

    def log_audit(db: Session, workspace_id: str, actor: str, action: str, target_type: str, target_id: str, details: dict[str, Any] | None = None) -> None:
        db.add(
            AuditLog(
                workspace_id=workspace_id,
                actor=actor,
                action=action,
                target_type=target_type,
                target_id=target_id,
                details=details or {},
            )
        )

    def run_executor(run_id: str) -> None:
        with SessionLocal() as db:
            run = db.get(Run, run_id)
            if run is None:
                return
            task = db.get(Task, run.task_id)
            if task is None:
                return
            run.status = "running"
            task.status = "running"
            db.add(RunEvent(run_id=run.id, event_type="run.started", payload={"task_id": task.id}))
            log_audit(db, run.workspace_id, "system", "run_started", "run", run.id)
            db.commit()

            result = {
                "status": "success",
                "summary": f"Completed objective: {task.objective}",
                "artifacts": [],
                "evidence": [{"type": "execution", "message": "Task executed by minimal runtime"}],
                "tool_calls": [
                    {
                        "tool": tool,
                        "status": "simulated",
                    }
                    for tool in task.permitted_tools
                ],
                "warnings": [],
                "errors": [],
                "recommended_next_actions": ["review_run", "request_approval_if_needed"],
            }

            artifact_path = artifact_dir / run.workspace_id / run.id / "result.json"
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            payload_text = json.dumps(result, ensure_ascii=False, indent=2)
            artifact_path.write_text(payload_text, encoding="utf-8")
            artifact = Artifact(
                id=_id(),
                run_id=run.id,
                workspace_id=run.workspace_id,
                artifact_type="run_result",
                path=str(artifact_path),
                checksum=str(abs(hash(payload_text))),
            )
            db.add(artifact)
            result["artifacts"].append({"id": artifact.id, "path": artifact.path, "type": artifact.artifact_type})

            run.status = "completed"
            task.status = "completed"
            run.completed_at = utcnow()
            run.summary = result["summary"]
            run.result_payload = result
            db.add(RunEvent(run_id=run.id, event_type="run.completed", payload={"status": "completed"}))
            log_audit(db, run.workspace_id, "system", "run_completed", "run", run.id, {"status": run.status})
            db.commit()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/api/v1/workspaces")
    def create_workspace(payload: WorkspaceCreate) -> dict[str, Any]:
        with SessionLocal() as db:
            workspace = Workspace(id=_id(), name=payload.name, description=payload.description)
            db.add(workspace)
            log_audit(db, workspace.id, "user", "workspace_created", "workspace", workspace.id)
            db.commit()
            return {"id": workspace.id, "name": workspace.name, "description": workspace.description}

    @app.post("/api/v1/model-providers")
    def create_model_provider(payload: ModelProviderCreate) -> dict[str, Any]:
        with SessionLocal() as db:
            if db.get(Workspace, payload.workspace_id) is None:
                raise HTTPException(status_code=404, detail="workspace not found")
            provider = ModelProvider(id=_id(), **payload.model_dump())
            db.add(provider)
            log_audit(db, payload.workspace_id, "user", "model_provider_registered", "model_provider", provider.id)
            db.commit()
            return {"id": provider.id, "kind": provider.kind, "name": provider.name}

    @app.post("/api/v1/tools")
    def create_tool(payload: ToolCreate) -> dict[str, Any]:
        with SessionLocal() as db:
            if db.get(Workspace, payload.workspace_id) is None:
                raise HTTPException(status_code=404, detail="workspace not found")
            tool = Tool(id=_id(), **payload.model_dump())
            db.add(tool)
            log_audit(db, payload.workspace_id, "user", "tool_connected", "tool", tool.id, {"tool_type": tool.tool_type})
            db.commit()
            return {"id": tool.id, "name": tool.name, "tool_type": tool.tool_type, "enabled": tool.enabled}

    @app.post("/api/v1/mcp-servers")
    def create_mcp_server(payload: ToolCreate) -> dict[str, Any]:
        mcp_payload = payload.model_copy(update={"tool_type": "mcp_server"})
        return create_tool(mcp_payload)

    @app.get("/api/v1/mcp-servers")
    def list_mcp_servers(workspace_id: str) -> list[dict[str, Any]]:
        with SessionLocal() as db:
            rows = db.query(Tool).filter(Tool.workspace_id == workspace_id, Tool.tool_type == "mcp_server").all()
            return [
                {
                    "id": t.id,
                    "name": t.name,
                    "endpoint": t.endpoint,
                    "enabled": t.enabled,
                    "health": "unknown",
                }
                for t in rows
            ]

    @app.post("/api/v1/agents")
    def create_agent(payload: AgentCreate) -> dict[str, Any]:
        with SessionLocal() as db:
            if db.get(Workspace, payload.workspace_id) is None:
                raise HTTPException(status_code=404, detail="workspace not found")
            if db.get(ModelProvider, payload.model_provider_id) is None:
                raise HTTPException(status_code=404, detail="model provider not found")
            for tool_id in payload.tool_ids:
                if db.get(Tool, tool_id) is None:
                    raise HTTPException(status_code=404, detail=f"tool not found: {tool_id}")
            agent = Agent(id=_id(), **payload.model_dump())
            db.add(agent)
            log_audit(db, payload.workspace_id, "user", "agent_created", "agent", agent.id)
            db.commit()
            return {"id": agent.id, "name": agent.name, "capabilities": agent.capabilities}

    @app.post("/api/v1/tasks")
    def submit_task(payload: TaskCreate, background_tasks: BackgroundTasks) -> dict[str, Any]:
        if payload.depth > 4:
            raise HTTPException(status_code=400, detail="delegation depth exceeded")
        with SessionLocal() as db:
            if db.get(Workspace, payload.workspace_id) is None:
                raise HTTPException(status_code=404, detail="workspace not found")
            if db.get(Agent, payload.requesting_agent) is None or db.get(Agent, payload.assigned_agent) is None:
                raise HTTPException(status_code=404, detail="agent not found")

            task = Task(id=_id(), **payload.model_dump())
            run = Run(id=_id(), task_id=task.id, workspace_id=payload.workspace_id, status="queued")
            db.add(task)
            db.add(run)
            db.add(RunEvent(run_id=run.id, event_type="run.queued", payload={"priority": task.priority}))
            log_audit(db, payload.workspace_id, "user", "task_submitted", "task", task.id, {"run_id": run.id})
            db.commit()
            background_tasks.add_task(run_executor, run.id)
            return {"task_id": task.id, "run_id": run.id, "status": "queued"}

    @app.get("/api/v1/runs/{run_id}")
    def get_run(run_id: str) -> dict[str, Any]:
        with SessionLocal() as db:
            run = db.get(Run, run_id)
            if run is None:
                raise HTTPException(status_code=404, detail="run not found")
            return {
                "id": run.id,
                "task_id": run.task_id,
                "status": run.status,
                "summary": run.summary,
                "result": run.result_payload,
                "completed_at": run.completed_at,
            }

    @app.get("/api/v1/runs")
    def list_runs(workspace_id: str) -> list[dict[str, Any]]:
        with SessionLocal() as db:
            runs = db.query(Run).filter(Run.workspace_id == workspace_id).order_by(Run.created_at.desc()).all()
            return [{"id": r.id, "status": r.status, "task_id": r.task_id, "created_at": r.created_at} for r in runs]

    @app.get("/api/v1/runs/{run_id}/events")
    def list_run_events(run_id: str) -> list[dict[str, Any]]:
        with SessionLocal() as db:
            events = db.query(RunEvent).filter(RunEvent.run_id == run_id).order_by(RunEvent.id.asc()).all()
            return [
                {
                    "id": e.id,
                    "event_type": e.event_type,
                    "payload": e.payload,
                    "created_at": e.created_at,
                }
                for e in events
            ]

    @app.get("/api/v1/runs/{run_id}/events/stream")
    def stream_run_events(run_id: str, last_event_id: int = Query(default=0)) -> StreamingResponse:
        def event_stream() -> Any:
            with SessionLocal() as db:
                events = (
                    db.query(RunEvent)
                    .filter(RunEvent.run_id == run_id, RunEvent.id > last_event_id)
                    .order_by(RunEvent.id.asc())
                    .all()
                )
                for event in events:
                    payload = json.dumps({"id": event.id, "type": event.event_type, "payload": event.payload}, ensure_ascii=False)
                    yield f"id: {event.id}\nevent: {event.event_type}\ndata: {payload}\n\n"
        return StreamingResponse(event_stream(), media_type="text/event-stream")

    @app.get("/api/v1/artifacts")
    def list_artifacts(run_id: str) -> list[dict[str, Any]]:
        with SessionLocal() as db:
            rows = db.query(Artifact).filter(Artifact.run_id == run_id).order_by(Artifact.created_at.asc()).all()
            return [{"id": a.id, "path": a.path, "artifact_type": a.artifact_type, "checksum": a.checksum} for a in rows]

    @app.get("/api/v1/audit-logs")
    def list_audit_logs(workspace_id: str) -> list[dict[str, Any]]:
        with SessionLocal() as db:
            rows = db.query(AuditLog).filter(AuditLog.workspace_id == workspace_id).order_by(AuditLog.id.asc()).all()
            return [
                {
                    "id": r.id,
                    "actor": r.actor,
                    "action": r.action,
                    "target_type": r.target_type,
                    "target_id": r.target_id,
                    "details": r.details,
                    "created_at": r.created_at,
                }
                for r in rows
            ]

    return app


app = create_app(
    database_url=os.getenv("DATABASE_URL", "sqlite:///./agenthub.db"),
    artifact_root=os.getenv("ARTIFACT_ROOT", "./artifacts"),
)
