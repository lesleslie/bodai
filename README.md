# Bodai - The Orb

[![Code style: crackerjack](https://img.shields.io/badge/code%20style-crackerjack-000042)](https://github.com/lesleslie/crackerjack)
[![Runtime: oneiric](https://img.shields.io/badge/runtime-oneiric-6e5494)](https://github.com/lesleslie/oneiric)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python: 3.13+](https://img.shields.io/badge/python-3.13%2B-green)](https://www.python.org/downloads/)

Central meta-project for the Bodai ecosystem, providing configuration, documentation, and operations for all components.

> **ORB**: *Orchestrated Reasoning Brain*
>
> *Perceive. Reason. Orchestrate.*

> **Etymology**: From Sanskrit *bodhi* (awakening, enlightenment) - the state of supreme understanding.

## Quick Links

- [Ecosystem Components](#ecosystem-components)
- [Mahavishnu - The Orchestrator](#mahavishnu---the-orchestrator)
- [Akosha - The Seer](#akosha---the-seer)
- [Dhara - The Curator](#dhara---the-curator)
- [Session-Buddy - The Builder](#session-buddy---the-builder)
- [Crackerjack - The Inspector](#crackerjack---the-inspector)

## Quality & CI

Crackerjack is the Bodai ecosystem's standard quality-control and CI/CD runner. Repo-level quality gates should align with Crackerjack workflows unless a repo documents an exception.

## Ecosystem Components

The Bodai ecosystem consists of six interconnected components, each with a distinct role. Five are network services with MCP servers, while Oneiric serves as a shared library.

| Component | Role | Port | GitHub | Description |
|-----------|------|------|--------|-------------|
| [Mahavishnu](#mahavishnu---the-orchestrator) | Orchestrator | 8680 | [lesleslie/mahavishnu](https://github.com/lesleslie/mahavishnu) | Multi-engine workflow orchestration |
| [Akosha](#akosha---the-seer) | Seer | 8682 | [lesleslie/akosha](https://github.com/lesleslie/akosha) | Cross-system intelligence & vector embeddings |
| [Dhara](#dhara---the-curator) | Curator | 8683 | [lesleslie/dhara](https://github.com/lesleslie/dhara) | Persistent object storage with ACID |
| [Session-Buddy](#session-buddy---the-builder) | Builder | 8678 | [lesleslie/session-buddy](https://github.com/lesleslie/session-buddy) | Session lifecycle & knowledge graphs |
| [Crackerjack](#crackerjack---the-inspector) | Inspector | 8676 | [lesleslie/crackerjack](https://github.com/lesleslie/crackerjack) | Quality gates & CI/CD validation |
| [Oneiric](#oneiric---the-foundation) | Foundation | N/A | [lesleslie/oneiric](https://github.com/lesleslie/oneiric) | Component resolution, lifecycle management, adapter system, action kits, domain bridges, runtime orchestration, remote delivery |

---

### Mahavishnu - The Orchestrator

> From Sanskrit *maha* (great) + *Vishnu* (the preserver in Hindu trinity)

The central workflow engine that routes tasks to appropriate execution engines, coordinates multi-step processes across components, and manages workflow definitions and templates.

- Routes tasks to Akosha for intelligence operations
- Persists state to Dhara for recovery
- Tracks context in Session-Buddy
- Validates with Crackerjack before execution

### Akosha - The Seer

> From Sanskrit *akasha* (sky, ether, space) - the fifth element, medium of consciousness

Provides cross-system intelligence through vector embeddings, semantic search, pattern detection, and knowledge graphs. Enables predictive analysis and recommendations across all sessions.

- Receives session data from Session-Buddy for embedding
- Stores patterns in Dhara
- Provides intelligence to Mahavishnu
- Receives code analysis from Crackerjack

### Dhara - The Curator

> From Sanskrit *dhara* (firm, constant, unchanging) - also the Pole Star

The single source of truth for persistent data. Provides ACID transaction guarantees, data versioning, backup/recovery, and efficient querying.

- Stores state for Mahavishnu
- Persists patterns for Akosha
- Backs up sessions for Session-Buddy
- Stores quality reports for Crackerjack

### Session-Buddy - The Builder

The session lifecycle manager that tracks conversation history, builds knowledge graphs, and enables context switching between sessions.

- Sends data to Akosha for embedding
- Stores backups in Dhara
- Provides context to Mahavishnu
- Receives quality metrics from Crackerjack

### Crackerjack - The Inspector

The quality enforcer that runs automated test suites, manages CI/CD pipelines, provides code analysis and linting, and tracks quality metrics over time.

- Validates workflows for Mahavishnu
- Sends code analysis to Akosha
- Stores reports in Dhara
- Records metrics in Session-Buddy

### Oneiric - The Foundation

> From Greek *oneiros* (dream) - relating to dreams, the abstract and complex

The platform foundation library that provides explainable component resolution, lifecycle management, an adapter system spanning 18+ domains, action kits for automation, domain bridges (services/tasks/events/workflows), runtime orchestration, and remote delivery via signed manifests. Every other Bodai component builds on top of Oneiric's patterns.

- Used by Mahavishnu for layered configuration and lifecycle management
- Used by mcp-common as the Oneiric-native foundation for all MCP servers
- Used by Dhara for configuration, logging, and secrets management
- Used by Session-Buddy for storage adapters, configuration, and lifecycle
- Used by Crackerjack for runtime orchestration and health snapshots
- Used by Akosha for universal storage abstraction and adapter resolution

---

## Installation

```bash
uv sync
```

## Commands

Bodai provides a unified CLI for managing the ecosystem:

| Command | Description |
|---------|-------------|
| `bodai health` | Check health status of all ecosystem components |
| `bodai start` | Start all ecosystem services |
| `bodai stop` | Stop all ecosystem services |
| `bodai restart` | Restart all ecosystem services |
| `bodai dashboard` | Launch the interactive monitoring dashboard |
| `bodai shell` | Open an interactive management shell |
| `bodai config show` | Display current configuration |
| `bodai config validate` | Validate configuration files |

## Architecture

For detailed architecture documentation, see [docs/architecture.md](docs/architecture.md).

## Development

### Running Tests

```bash
pytest
```

### Quality Checks

```bash
crackerjack run
```

## Related Documentation

- [Architecture](docs/architecture.md) - System overview and data flow
- [Component Roles](docs/roles.md) - Detailed descriptions of each component
- [Symbiosis](docs/symbiosis.md) - How components work together
- [Port Map](docs/portmap.md) - Port allocation and rationale

## Claude Code marketplace

The five Bodai MCP-server plugins are distributed via the `bodai-plugins` marketplace:

```bash
claude plugin marketplace add https://github.com/lesleslie/bodai-plugins
claude plugin install mahavishnu
claude plugin install session-buddy
claude plugin install crackerjack
claude plugin install akosha
claude plugin install dhara
```

Each plugin ships its own slash commands under the `<server>:<command>` namespace (e.g. `/mahavishnu:status`, `/session-buddy:checkpoint`).
