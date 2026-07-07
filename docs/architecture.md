# AgentHub Architecture

## Design Goal

AgentHub is a self-hosted AI control plane. It owns identity, context, memory, policy, routing, execution state, artifacts, and auditability. External AI tools become clients.

## System Overview

```text
Client / AI Tool
      |
      v
AgentHub API
      |
      +-- Context Engine
      +-- Agent Registry
      +-- Skill Registry
      +-- Provider Gateway
      +-- Tool / MCP Gateway
      +-- Run Engine
      +-- Artifact Store
      +-- Audit Log
      |
      +-- PostgreSQL
      +-- Redis
      +-- Object/File Storage
```

## Legacy Approach

A modular monolith using FastAPI, PostgreSQL, Redis, Docker Compose, filesystem-backed registry import/export, and SSE is the right first implementation. It is simple to operate on a VPS and easy to debug.

## Modern Approach

The optimized version can split Provider Gateway, Tool Gateway, Run Engine, Memory Service, and Agent Runtime into independent services with durable workflows, policy-as-code, distributed tracing, and object storage.

## Recommended Boundary

AgentHub should own:

- context assembly
- identity resolution
- workspace scoping
- memory retrieval and persistence
- provider routing
- tool authorization
- run orchestration
- artifacts
- audit events

AI clients should not own persistent memory or bypass tool policy.

## Context Assembly Pipeline

```text
Incoming request
  -> identity resolution
  -> workspace resolution
  -> conversation context
  -> core memory retrieval
  -> persistent memory retrieval
  -> user profile resolution
  -> agent selection
  -> skill resolution
  -> tool capability resolution
  -> policy filtering
  -> token budgeting
  -> context package
  -> agent execution
  -> memory extraction
  -> artifact persistence
  -> audit event
```

## Core Design Pattern

Use a control-plane/data-plane split:

- Control plane: registries, policy, configuration, audit, workspace model.
- Data plane: actual model calls, tool calls, MCP invocation, artifacts, and run event streams.
