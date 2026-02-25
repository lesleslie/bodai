# Bodai Ecosystem Meta-Project Design

**Date:** 2026-02-20
**Status:** Approved
**Author:** Claude + User

## Overview

Bodai (The Orb) is the meta-project that documents, configures, and operates the Bodai ecosystem. It serves as the central hub for understanding and managing the interconnected components that form the AI-assisted development environment.

## Ecosystem Components

| Component | Role | Port | Description |
|-----------|------|------|-------------|
| **Mahavishnu** | The Orchestrator | 8680 | Multi-engine workflow orchestration, pool management |
| **Akosha** | The Seer | 8682 | Cross-system intelligence, memory aggregation, pattern recognition |
| **Druva** | The Curator | 8683 | Persistent object storage with ACID properties |
| **Session-Buddy** | The Builder | 8678 | Session lifecycle management, knowledge graph construction |
| **Crackerjack** | The Inspector | 8676 | Quality gates, testing, CI/CD validation |
| **FastBlocks** | The Composer | 8684 | Block-based web framework and template composition |
| **SplashStand** | The Presenter | - | PWA and mini-CMS built on FastBlocks (proprietary) |
| **MDInject** | The Doctor | 8685 | Markdown injection, diagnosis, and content healing (proprietary) |
| **Oneiric** | The Resolver | - | Universal component resolution (library, no MCP server) |

**Note:** Oneiric's MCP server was absorbed into Druva. Port 8681 is available. SplashStand and MDInject are proprietary; all other components are BSD-3 licensed.

## Architecture

### Three Layers

| Layer | Purpose | Technology |
|-------|---------|------------|
| **Config** | Component registry, portmap, storage maps | Oneiric + YAML |
| **Docs** | Architecture, roles, symbiosis explanations | Markdown |
| **Operations** | Health checks, start/stop, dashboard | Typer CLI + Textual TUI + IPython |

### Relationship to Ecosystem

- Bodai does NOT import other components
- Other components CAN import Bodai's config (optional dependency)
- Bodai operates ON other components (starts, stops, checks health)
- Bodai uses Oneiric for its own config loading (dogfooding)

### Python Version

3.13+ (matches ecosystem)

## Directory Structure

```
bodai/
├── README.md                      # Ecosystem overview, quick reference
├── pyproject.toml                 # Project metadata, dependencies
├── CLAUDE.md                      # Development guidance
│
├── bodai/
│   ├── __init__.py
│   ├── cli.py                     # Typer CLI entry point
│   ├── tui/
│   │   ├── __init__.py
│   │   └── dashboard.py           # Textual TUI health dashboard
│   ├── admin/
│   │   ├── __init__.py
│   │   └── shell.py               # IPython admin shell
│   ├── core/
│   │   ├── __init__.py
│   │   ├── health.py              # Health check logic
│   │   ├── operations.py          # Start/stop/restart logic
│   │   └── config.py              # Oneiric config loader
│   └── models/
│       ├── __init__.py
│       └── ecosystem.py           # Pydantic models for components
│
├── config/
│   ├── ecosystem.yaml             # Component definitions (Oneiric-managed)
│   ├── portmap.yaml               # Port allocations
│   └── storage-map.yaml           # DB/storage/cache allocations
│
├── docs/
│   ├── architecture.md            # How components fit together
│   ├── roles.md                   # Role descriptions & responsibilities
│   ├── symbiosis.md               # How components work together
│   └── portmap.md                 # Port allocation rationale
│
└── tests/
    ├── __init__.py
    ├── test_health.py
    ├── test_operations.py
    └── test_config.py
```

## Config Layer

### Config Files

| File | Format | Purpose |
|------|--------|---------|
| `config/ecosystem.yaml` | YAML | Component registry with role, port, repo, status |
| `config/portmap.yaml` | YAML | Port allocations with ranges and rationale |
| `config/storage-map.yaml` | YAML | DB, cache, and storage assignments |

### Oneiric Integration

Bodai loads configs via Oneiric's layered resolution:

```python
# bodai/core/config.py
from oneiric import OneiricConfig

class BodaiConfig(OneiricConfig):
    """Bodai config loaded via Oneiric resolution."""
    ecosystem: EcosystemConfig
    portmap: PortmapConfig
    storage_map: StorageMapConfig
```

### Precedence (Oneiric 4-tier)

1. Explicit overrides (`BODAI_<FIELD>` env vars)
1. `config/local.yaml` (gitignored, local dev)
1. `config/ecosystem.yaml` (committed, shared)
1. Pydantic model defaults

### ecosystem.yaml Structure

```yaml
components:
  mahavishnu:
    role: orchestrator
    port: 8680
    repo: ~/Projects/mahavishnu
    status: production
    description: Multi-engine workflow orchestration

  akosha:
    role: seer
    port: 8682
    repo: ~/Projects/akosha
    status: production
    description: Cross-system intelligence

  druva:
    role: curator
    port: 8683
    repo: ~/Projects/druva
    status: production
    description: Persistent object storage with ACID

  session-buddy:
    role: builder
    port: 8678
    repo: ~/Projects/session-buddy
    status: production
    description: Session management and knowledge graphs

  crackerjack:
    role: inspector
    port: 8676
    repo: ~/Projects/crackerjack
    status: production
    description: Quality gates and CI/CD
```

## CLI Layer

### Commands

```bash
bodai health                    # Check all components, print status table
bodai health --watch            # Continuous health monitoring

bodai start                     # Start all components
bodai start mahavishnu akosha   # Start specific components

bodai stop                      # Stop all components
bodai stop crackerjack          # Stop specific component

bodai restart                   # Restart all components

bodai status                    # Show current status (cached)
bodai dashboard                 # Launch TUI health dashboard

bodai shell                     # Launch IPython admin shell

bodai config show               # Display current config
bodai config validate           # Validate all config files
```

### Health Check Output

```
       Bodai Ecosystem Health
┏━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Component    ┃ Port   ┃ Status  ┃ Role       ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━┩
│ mahavishnu   │ 8680   │ ●       │ Orchestrator│
│ akosha       │ 8682   │ ●       │ Seer       │
│ druva       │ 8683   │ ●       │ Curator    │
│ session-buddy│ 8678   │ ●       │ Builder    │
│ crackerjack  │ 8676   │ ●       │ Inspector  │
└──────────────┴────────┴─────────┴────────────┘
  ● healthy   ○ unhealthy   ◆ unknown
```

### Implementation

```python
# bodai/cli.py
import typer
from rich.console import Console
from bodai.core.health import check_all, check_component
from bodai.core.operations import start_all, start_components

app = typer.Typer(name="bodai", help="The Orb - Ecosystem meta-manager")
console = Console()

@app.command()
def health(watch: bool = False):
    """Check health of all ecosystem components."""
    ...

@app.command()
def start(components: list[str] = None):
    """Start ecosystem components."""
    ...

@app.command()
def stop(components: list[str] = None):
    """Stop ecosystem components."""
    ...

@app.command()
def dashboard():
    """Launch TUI health dashboard."""
    ...

@app.command()
def shell():
    """Launch IPython admin shell."""
    ...
```

## TUI Layer

### Technology

Textual (Python async TUI framework)

### Dashboard View

```
╭─────────────── Bodai Ecosystem Dashboard ───────────────╮
│ Refreshed: 2026-02-20 13:45:23          [q] Quit [r] Refresh │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ● Mahavishnu    [Orchestrator]    Port 8680   2h 15m   │
│    └─ Uptime: healthy, 3 active workflows               │
│                                                          │
│  ● Akosha        [Seer]           Port 8682   5h 30m   │
│    └─ 847 systems indexed, 12M embeddings               │
│                                                          │
│  ● Druva        [Curator]        Port 8683   1d 2h    │
│    └─ Storage: 2.3TB objects, 99.9% cache hit           │
│                                                          │
│  ● Session-Buddy [Builder]        Port 8678   4h 45m   │
│    └─ 23 active sessions, 1.2K reflections              │
│                                                          │
│  ● Crackerjack   [Inspector]      Port 8676   3d 12h   │
│    └─ Last run: 2m ago, all checks passed               │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Summary: 5/5 healthy   │   Press [h] for CLI commands   │
╰──────────────────────────────────────────────────────────╯
```

### Features

- Real-time health status with color coding (green/yellow/red)
- Uptime and component-specific metrics
- Auto-refresh every 30s (configurable)
- Keyboard shortcuts: `q` quit, `r` refresh, `h` help

### Implementation

```python
# bodai/tui/dashboard.py
from textual.app import App
from textual.widgets import Header, Footer, Static

class BodaiDashboard(App):
    """Bodai ecosystem health dashboard."""

    CSS_PATH = "dashboard.css"
    BINDINGS = [("q", "quit", "Quit"), ("r", "refresh", "Refresh")]

    def compose(self):
        yield Header()
        yield ComponentList()
        yield Footer()
```

## IPython Admin Shell

### Purpose

Interactive Python shell with pre-loaded Bodai context for ad-hoc ecosystem operations and debugging.

### Launch

```bash
bodai shell
```

### Implementation

```python
# bodai/admin/shell.py
from IPython import start_ipython
from rich import print

def launch_shell():
    """Launch IPython with Bodai context pre-loaded."""

    # Pre-loaded imports
    import bodai
    from bodai.core.config import BodaiConfig
    from bodai.core.health import check_all, check_component
    from bodai.core.operations import start_all, stop_all, start_component, stop_component
    from bodai.models.ecosystem import Component, Ecosystem

    # Load config
    config = BodaiConfig.load()
    ecosystem = config.ecosystem

    # Welcome banner
    print("[bold cyan]Bodai Admin Shell[/bold cyan]")
    print(f"  Ecosystem: {len(ecosystem.components)} components")
    print("  Pre-loaded: config, ecosystem, check_all, start_all, stop_all")
    print()

    start_ipython(argv=[], user_ns=locals())
```

### Usage Example

```python
In [1]: ecosystem.components
Out[1]:
{'mahavishnu': Component(role='orchestrator', port=8680, ...),
 'akosha': Component(role='seer', port=8682, ...),
 ...}

In [2]: check_all()
Out[2]: {'mahavishnu': True, 'akosha': True, 'druva': True, ...}

In [3]: stop_component('crackerjack')
Stopping crackerjack on port 8676...

In [4]: ecosystem.components['akosha'].model_dump()
```

### Magic Commands

Typer commands are automatically registered as IPython magic commands via Oneiric's admin shell integration.

## Documentation Structure

### README.md

Quick reference with component table, commands, and architecture link.

### docs/ Files

| File | Content |
|------|---------|
| `architecture.md` | System diagram (Mermaid), component boundaries, data flow |
| `roles.md` | Detailed role descriptions, responsibilities, metaphors |
| `symbiosis.md` | How components interact and depend on each other |
| `portmap.md` | Port allocation rationale, reserved ranges |

### symbiosis.md Interactions

- **Session-Buddy → Akosha**: Memory aggregation pipeline
- **Mahavishnu → All**: Orchestration and workflow scheduling
- **Oneiric → All**: Config resolution and hot-swapping
- **Druva → All**: Persistent storage backends
- **Crackerjack → All**: Quality gates and validation

## Dependencies

```toml
[project]
dependencies = [
    "oneiric>=0.2.0",
    "typer>=0.9.0",
    "rich>=13.0.0",
    "textual>=0.40.0",
    "ipython>=8.0.0",
    "pydantic>=2.0.0",
    "httpx>=0.25.0",  # For health checks
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
]
```

## Success Criteria

1. **Config**: Can load and validate ecosystem config via Oneiric
1. **Health**: Can check health of all components in \<5 seconds
1. **Operations**: Can start/stop all components from single command
1. **Dashboard**: TUI displays real-time health with auto-refresh
1. **Shell**: IPython shell has pre-loaded ecosystem context
1. **Docs**: Documentation explains ecosystem architecture clearly
