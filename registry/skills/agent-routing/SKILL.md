---
name: agent-routing
version: 0.1.0
description: Route work to specialist agents using explicit capability boundaries.
triggers:
  - route
  - delegate
  - specialist
---

# Agent Routing

Use explicit routing criteria:

1. Identify the requested outcome.
2. Identify required capabilities.
3. Check policy and workspace scope.
4. Select the narrowest capable specialist.
5. Preserve provenance in the run event log.
