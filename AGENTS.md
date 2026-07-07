# AgentHub AI Client Guide

AgentHub provides a governed context and execution layer for AI tools.

## Required Client Flow

1. Resolve workspace.
2. Request a context package from AgentHub.
3. Use only the agents, skills, tools, and memory included in that package.
4. Submit tool invocations through the Tool Gateway.
5. Report run events and artifacts back to AgentHub.
6. Do not persist private memory outside the approved memory scope.

## Memory Rules

Memory access is scoped by:

```text
user_id + workspace_id + namespace + classification
```

Agents must not assume that all user memory is globally available.

## Tool Rules

Tools and MCP servers are capability-scoped. A registered tool is not automatically available to every agent.

## Output Rules

Runs should produce:

- events
- artifacts
- audit entries
- optional memory extraction candidates
