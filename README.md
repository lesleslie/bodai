# Bodai

Central meta-project for the Bodai ecosystem, providing configuration, documentation, and operations for all components.

> **ORB**: *Orchestrated Reasoning Brain*
>
> *Perceive. Reason. Orchestrate.*

> **Etymology**: From Sanskrit *bodhi* (awakening, enlightenment) - the state of supreme understanding.

## Ecosystem Components

The Bodai ecosystem consists of six interconnected components, each with a distinct role. Five are network services with MCP servers, while Oneiric serves as a shared library.

| Component | Role | Port | GitHub | Description |
|-----------|------|------|--------|-------------|
| [Mahavishnu](#mahavishnu---the-orchestrator) | Orchestrator | 8680 | [lesleslie/mahavishnu](https://github.com/lesleslie/mahavishnu) | Multi-engine workflow orchestration |
| [Akosha](#akosha---the-seer) | Seer | 8682 | [lesleslie/akosha](https://github.com/lesleslie/akosha) | Cross-system intelligence & vector embeddings |
| [Druva](#druva---the-curator) | Curator | 8683 | [lesleslie/druva](https://github.com/lesleslie/druva) | Persistent object storage with ACID |
| [Session-Buddy](#session-buddy---the-builder) | Builder | 8678 | [lesleslie/session-buddy](https://github.com/lesleslie/session-buddy) | Session lifecycle & knowledge graphs |
| [Crackerjack](#crackerjack---the-inspector) | Inspector | 8676 | [lesleslie/crackerjack](https://github.com/lesleslie/crackerjack) | Quality gates & CI/CD validation |
| [Oneiric](#oneiric---the-resolver) | Resolver | N/A | [lesleslie/oneiric](https://github.com/lesleslie/oneiric) | Conflict resolution library |

---

### Mahavishnu - The Orchestrator

> From Sanskrit *maha* (great) + *Vishnu* (the preserver in Hindu trinity)

The central workflow engine that routes tasks to appropriate execution engines, coordinates multi-step processes across components, and manages workflow definitions and templates.

- Routes tasks to Akosha for intelligence operations
- Persists state to Druva for recovery
- Tracks context in Session-Buddy
- Validates with Crackerjack before execution

### Akosha - The Seer

> From Sanskrit *akasha* (sky, ether, space) - the fifth element, medium of consciousness

Provides cross-system intelligence through vector embeddings, semantic search, pattern detection, and knowledge graphs. Enables predictive analysis and recommendations across all sessions.

- Receives session data from Session-Buddy for embedding
- Stores patterns in Druva
- Provides intelligence to Mahavishnu
- Receives code analysis from Crackerjack

### Druva - The Curator

> From Sanskrit *druva* (firm, constant, unchanging) - also the Pole Star

The single source of truth for persistent data. Provides ACID transaction guarantees, data versioning, backup/recovery, and efficient querying.

- Stores state for Mahavishnu
- Persists patterns for Akosha
- Backs up sessions for Session-Buddy
- Stores quality reports for Crackerjack

### Session-Buddy - The Builder

The session lifecycle manager that tracks conversation history, builds knowledge graphs, and enables context switching between sessions.

- Sends data to Akosha for embedding
- Stores backups in Druva
- Provides context to Mahavishnu
- Receives quality metrics from Crackerjack

### Crackerjack - The Inspector

The quality enforcer that runs automated test suites, manages CI/CD pipelines, provides code analysis and linting, and tracks quality metrics over time.

- Validates workflows for Mahavishnu
- Sends code analysis to Akosha
- Stores reports in Druva
- Records metrics in Session-Buddy

### Oneiric - The Resolver

> From Greek *oneiros* (dream) - relating to dreams, the abstract and complex

A shared library (no MCP server) that provides conflict resolution algorithms, dependency graph analysis, version conflict detection, and merge strategies. Embedded directly by other components.

- Used by Mahavishnu for workflow conflict resolution
- Used by Druva for data merge operations
- Used by Session-Buddy for context merging

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
