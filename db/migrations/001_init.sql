CREATE TABLE IF NOT EXISTS workspaces (
  id UUID PRIMARY KEY,
  name VARCHAR(120) NOT NULL UNIQUE,
  description TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS model_providers (
  id UUID PRIMARY KEY,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  name VARCHAR(120) NOT NULL,
  kind VARCHAR(60) NOT NULL,
  endpoint VARCHAR(255),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tools (
  id UUID PRIMARY KEY,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  name VARCHAR(120) NOT NULL,
  tool_type VARCHAR(60) NOT NULL,
  endpoint VARCHAR(255),
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agents (
  id UUID PRIMARY KEY,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  name VARCHAR(120) NOT NULL,
  description TEXT,
  model_provider_id UUID NOT NULL REFERENCES model_providers(id),
  instructions JSONB NOT NULL DEFAULT '[]'::jsonb,
  capabilities JSONB NOT NULL DEFAULT '[]'::jsonb,
  tool_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tasks (
  id UUID PRIMARY KEY,
  parent_task_id UUID,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  requesting_agent UUID NOT NULL REFERENCES agents(id),
  assigned_agent UUID NOT NULL REFERENCES agents(id),
  objective TEXT NOT NULL,
  required_context JSONB NOT NULL DEFAULT '{}'::jsonb,
  permitted_tools JSONB NOT NULL DEFAULT '[]'::jsonb,
  constraints JSONB NOT NULL DEFAULT '{}'::jsonb,
  expected_output_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
  timeout_seconds INTEGER NOT NULL DEFAULT 300,
  priority INTEGER NOT NULL DEFAULT 5,
  trace_id VARCHAR(64) NOT NULL,
  depth INTEGER NOT NULL DEFAULT 0,
  status VARCHAR(20) NOT NULL DEFAULT 'queued',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS runs (
  id UUID PRIMARY KEY,
  task_id UUID NOT NULL UNIQUE REFERENCES tasks(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  status VARCHAR(20) NOT NULL DEFAULT 'queued',
  summary TEXT,
  result_payload JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS run_events (
  id BIGSERIAL PRIMARY KEY,
  run_id UUID NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  event_type VARCHAR(60) NOT NULL,
  payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS artifacts (
  id UUID PRIMARY KEY,
  run_id UUID NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  artifact_type VARCHAR(60) NOT NULL,
  path VARCHAR(255) NOT NULL,
  checksum VARCHAR(64) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id BIGSERIAL PRIMARY KEY,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  actor VARCHAR(120) NOT NULL,
  action VARCHAR(120) NOT NULL,
  target_type VARCHAR(60) NOT NULL,
  target_id UUID NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
