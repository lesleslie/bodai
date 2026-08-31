# Bodai Ecosystem Integration

This document explains how the six core components of the Bodai ecosystem fit together to form the **Bodai Orb** (*Orchestrated Reasoning Brain*). It is the recommended starting point for understanding cross-component behavior; each component's own README documents its standalone capabilities.

> **Bodai Orb** — *Orchestrated Reasoning Brain*
>
> *Perceive. Reason. Orchestrate.*

______________________________________________________________________

## At a Glance

| Component | Role | Port | Standalone Capability | Ecosystem Role |
|-----------|------|------|----------------------|----------------|
| [mahavishnu](https://github.com/lesleslie/mahavishnu) | Orchestrator | 8680 | Multi-repo workflow orchestration | Routes work across all other components; manages worker pools |
| [akosha](https://github.com/lesleslie/akosha) | Seer | 8682 | Cross-system embeddings and semantic search | Provides intelligence layer used by every other component |
| [dhara](https://github.com/lesleslie/dhara) | Curator | 8683 | Persistent object storage with ACID | Backs adapter configs, lifecycle state, and event logs |
| [session-buddy](https://github.com/lesleslie/session-buddy) | Builder | 8678 | Session lifecycle and knowledge graphs | Persists conversation context across the ecosystem |
| [crackerjack](https://github.com/lesleslie/crackerjack) | Inspector | 8676 | Python quality gates and CI/CD | Runs as the quality standard for every Bodai repo |
| [oneiric](https://github.com/lesleslie/oneiric) | Resolver / Runtime | N/A | Component resolution and lifecycle | Foundation every component depends on for adapter registration |

See [`portmap.md`](portmap.md) for full port assignments and [`architecture.md`](architecture.md) for the dependency diagram.

______________________________________________________________________

## Core Principle: Each Component Is Runnable on Its Own

Every component in the Bodai ecosystem is designed to be useful independently. The "Bodai Orb" is the emergent behavior when they run together — **not** a hard requirement. If you only need:

- A workflow orchestrator → use **mahavishnu** alone
- A quality tool for Python projects → use **crackerjack** alone
- A persistent object store → use **dhara** alone
- A session memory server → use **session-buddy** alone
- A vector search service → use **akosha** alone
- A component resolution library → use **oneiric** alone

The ecosystem integrations described below are added on top, not built into the core.

______________________________________________________________________

## How Components Integrate

### Layer 1: Runtime Foundation — Oneiric

**Oneiric** is the bedrock. Every other component uses it to:

- Register adapters, services, tasks, events, and workflows
- Resolve which implementation to use at runtime (deterministic 4-tier precedence)
- Manage component lifecycle (start, stop, hot-swap)
- Stream telemetry and lifecycle events

Without Oneiric, the components have no shared vocabulary for "an adapter" or "a service." With it, they share a consistent registry, explainable resolution, and event bus.

### Layer 2: Persistence — Dhara

**Dhara** provides ACID storage that components use for:

- Adapter configurations registered through Oneiric
- Lifecycle checkpoints
- Event logs and replay buffers
- Service state that must survive restarts

Components can run without Dhara using ephemeral or local-file backends, but cross-component persistence only works when Dhara is available.

### Layer 3: Intelligence — Akosha

**Akosha** indexes and searches across:

- Source code from any registered repository
- Documentation and design artifacts
- Conversation context from Session-Buddy
- Workflow results from Mahavishnu

When Akosha is online, every other component can ask "what do we already know about X?" via semantic search instead of relying on literal text matching.

### Layer 4: Coordination — Mahavishnu

**Mahavishnu** is the active conductor. It:

- Receives tasks from users or other components
- Routes them through worker pools (local, Docker, cloud, AI-capable backends)
- Sweeps workflows across multiple repositories
- Manages lifecycle of all the other ecosystem services

Mahavishnu can run alone, but gains memory (via Dhara), intelligence (via Akosha), and context (via Session-Buddy) when those are present.

### Layer 5: Memory — Session-Buddy

**Session-Buddy** captures, indexes, and recovers the conversation context that flows through the rest of the stack. Its knowledge graph records:

- Agent selection decisions and rationale
- Cross-session decisions and their outcomes
- Quality issues caught by Crackerjack and how they were resolved
- Workflow runs and their results

Other components can write to Session-Buddy; Mahavishnu uses it to resume interrupted workflows.

### Layer 6: Quality — Crackerjack

**Crackerjack** is the only component that runs *on* the others rather than alongside them. Every Bodai repo uses Crackerjack for:

- Linting, typing, tests, security
- AI-assisted fixing via its MCP integration
- Release and publishing workflows

When Crackerjack runs in CI for a Bodai repo, it validates that the repo still works with the latest versions of the other components.

______________________________________________________________________

## Typical Request Flow

When a user issues a high-level command to the Bodai Orb (for example, "sweep the workflow `nightly-audit` across all Bodai repos"):

1. **Mahavishnu** receives the command and resolves which worker pool to use.
2. **Oneiric** resolves the adapter for the sweep target (priority, stack context, etc.).
3. **Dhara** persists the sweep's state so it can be checkpointed and resumed.
4. **Akosha** answers any "have we seen this before?" lookups the workflow needs.
5. **Session-Buddy** records the start of the sweep, agent selections, and any errors.
6. **Crackerjack** validates each affected repo before and after the workflow runs.
7. Results flow back to the user, with Session-Buddy retaining the full context.

This flow is the canonical pattern. Individual workflows can skip steps they don't need.

______________________________________________________________________

## Running Components Together

### Minimal "Quick Start"

The fastest way to feel the Orb in action:

```bash
# Start the orchestrator (this brings up Akosha, Dhara, Session-Buddy, Crackerjack)
mahavishnu start

# Confirm everything is healthy
mahavishnu health

# Run a sweep
mahavishnu sweep --workflow nightly-audit --tag bodai-core
```

When started this way, Mahavishnu orchestrates the others as worker processes. They communicate over the ports listed in [`portmap.md`](portmap.md).

### Manual / Distributed Setup

For larger deployments, each component can run on its own host:

```bash
# On host "storage"
dhara start

# On host "intelligence"
akosha start --dhara-url=http://storage:8683

# On host "memory"
session-buddy start --akosha-url=http://intelligence:8682

# On host "control"
mahavishnu start --dhara-url=http://storage:8683 \
                 --akosha-url=http://intelligence:8682 \
                 --session-buddy-url=http://memory:8678
```

Crackerjack is typically run on-demand per repository rather than as a long-running service, unless you want its MCP server always available.

______________________________________________________________________

## Where to Go Next

- **Understand the components in depth:** [`roles.md`](roles.md) has detailed responsibilities, ports, and interaction diagrams for each.
- **See the architecture:** [`architecture.md`](architecture.md) has Mermaid diagrams of the dependency graph.
- **Wire a new component into the ecosystem:** see [`druva_wiring.md`](druva_wiring.md) for the persistence wiring pattern, or refer to Oneiric's docs on adapter registration.
- **Plan a workflow:** Mahavishnu's [workflow authoring docs](https://github.com/lesleslie/mahavishnu) cover how to write sweeps and tasks that compose the other components.

______________________________________________________________________

## Adding Your Own Integration

If you maintain a tool or service that wants to participate in the Bodai Orb:

1. **Register an adapter with Oneiric** so the resolver knows about your service.
2. **Store any persistent state in Dhara** so other components can recover it.
3. **Emit events to the shared bus** (via Oneiric's event domain) so Mahavishnu can react.
4. **Capture decision context in Session-Buddy** so future sessions benefit.
5. **Validate with Crackerjack** before shipping.

You don't have to do all five — pick the ones that fit your service. The Orb is opt-in by design.