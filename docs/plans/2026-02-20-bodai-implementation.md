# Bodai Ecosystem Meta-Project Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the Bodai meta-project with config layer, CLI, TUI dashboard, IPython shell, and documentation.

**Architecture:** Three-layer design - Config (Oneiric + YAML), Docs (Markdown), Operations (Typer + Textual + IPython). Bodai is a passive reference that other components can optionally import for config.

**Tech Stack:** Python 3.13+, Oneiric, Typer, Rich, Textual, IPython, Pydantic, httpx, pytest

______________________________________________________________________

## Phase 1: Project Setup & Models

### Task 1: Update pyproject.toml

**Files:**

- Modify: `pyproject.toml`

**Step 1: Update project configuration**

```toml
[project]
name = "bodai"
version = "0.1.0"
description = "The Orb - Ecosystem meta-project for Bodai"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "oneiric>=0.2.0",
    "typer>=0.9.0",
    "rich>=13.0.0",
    "textual>=0.40.0",
    "ipython>=8.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "httpx>=0.25.0",
    "pyyaml>=6.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
]

[project.scripts]
bodai = "bodai.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Step 2: Verify syntax**

Run: `python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"`
Expected: No output (success)

**Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "chore: configure project dependencies and entry point"
```

______________________________________________________________________

### Task 2: Create package structure

**Files:**

- Create: `bodai/__init__.py`
- Create: `bodai/core/__init__.py`
- Create: `bodai/models/__init__.py`
- Create: `bodai/tui/__init__.py`
- Create: `bodai/admin/__init__.py`
- Create: `tests/__init__.py`

**Step 1: Create directories**

```bash
mkdir -p bodai/core bodai/models bodai/tui bodai/admin config tests
```

**Step 2: Create __init__.py files**

`bodai/__init__.py`:

```python
"""Bodai - The Orb. Ecosystem meta-project."""

__version__ = "0.1.0"
```

`bodai/core/__init__.py`:

```python
"""Core functionality: config, health, operations."""
```

`bodai/models/__init__.py`:

```python
"""Pydantic models for ecosystem configuration."""
```

`bodai/tui/__init__.py`:

```python
"""TUI components for dashboard."""
```

`bodai/admin/__init__.py`:

```python
"""Admin tools: IPython shell."""
```

`tests/__init__.py`:

```python
"""Tests for Bodai."""
```

**Step 3: Verify import**

Run: `python -c "import bodai; print(bodai.__version__)"`
Expected: `0.1.0`

**Step 4: Commit**

```bash
git add bodai/ tests/
git commit -m "chore: create package structure"
```

______________________________________________________________________

### Task 3: Create ecosystem Pydantic models

**Files:**

- Create: `bodai/models/ecosystem.py`
- Create: `tests/test_models.py`

**Step 1: Write the failing test**

`tests/test_models.py`:

```python
"""Tests for ecosystem models."""

import pytest
from bodai.models.ecosystem import Component, Ecosystem, ComponentStatus, ComponentRole


def test_component_creation():
    """Test creating a component."""
    component = Component(
        name="mahavishnu",
        role=ComponentRole.ORCHESTRATOR,
        port=8680,
        repo="~/Projects/mahavishnu",
        status=ComponentStatus.PRODUCTION,
        description="Multi-engine workflow orchestration",
    )
    assert component.name == "mahavishnu"
    assert component.port == 8680
    assert component.role == ComponentRole.ORCHESTRATOR


def test_ecosystem_creation():
    """Test creating an ecosystem with components."""
    ecosystem = Ecosystem(
        components={
            "mahavishnu": Component(
                name="mahavishnu",
                role=ComponentRole.ORCHESTRATOR,
                port=8680,
                repo="~/Projects/mahavishnu",
                status=ComponentStatus.PRODUCTION,
                description="Orchestrator",
            ),
            "akosha": Component(
                name="akosha",
                role=ComponentRole.SEER,
                port=8682,
                repo="~/Projects/akosha",
                status=ComponentStatus.PRODUCTION,
                description="Seer",
            ),
        }
    )
    assert len(ecosystem.components) == 2
    assert "mahavishnu" in ecosystem.components


def test_component_role_display():
    """Test role display name."""
    component = Component(
        name="test",
        role=ComponentRole.ORCHESTRATOR,
        port=8000,
        repo="~/test",
        status=ComponentStatus.PRODUCTION,
        description="Test",
    )
    assert component.role_display == "Orchestrator"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_models.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'bodai.models.ecosystem'"

**Step 3: Write the implementation**

`bodai/models/ecosystem.py`:

```python
"""Pydantic models for ecosystem configuration."""

from enum import Enum

from pydantic import BaseModel, Field


class ComponentRole(str, Enum):
    """Role of a component in the ecosystem."""

    ORCHESTRATOR = "orchestrator"
    SEER = "seer"
    RESOLVER = "resolver"
    CURATOR = "curator"
    BUILDER = "builder"
    INSPECTOR = "inspector"


class ComponentStatus(str, Enum):
    """Status of a component."""

    PRODUCTION = "production"
    DEVELOPMENT = "development"
    DISABLED = "disabled"


class Component(BaseModel):
    """A component in the Bodai ecosystem."""

    name: str
    role: ComponentRole
    port: int = Field(ge=1, le=65535)
    repo: str
    status: ComponentStatus = ComponentStatus.PRODUCTION
    description: str = ""

    @property
    def role_display(self) -> str:
        """Return display name for role."""
        return self.role.value.title()


class Ecosystem(BaseModel):
    """The complete Bodai ecosystem."""

    components: dict[str, Component] = Field(default_factory=dict)

    def get_by_port(self, port: int) -> Component | None:
        """Get component by port number."""
        for component in self.components.values():
            if component.port == port:
                return component
        return None

    def get_by_role(self, role: ComponentRole) -> Component | None:
        """Get component by role."""
        for component in self.components.values():
            if component.role == role:
                return component
        return None
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_models.py -v`
Expected: 3 passed

**Step 5: Commit**

```bash
git add bodai/models/ecosystem.py tests/test_models.py
git commit -m "feat: add ecosystem Pydantic models"
```

______________________________________________________________________

### Task 4: Create config models

**Files:**

- Create: `bodai/models/config.py`
- Modify: `tests/test_models.py`

**Step 1: Write the failing test**

Add to `tests/test_models.py`:

```python
from bodai.models.config import PortmapConfig, StorageMapConfig


def test_portmap_config():
    """Test portmap configuration."""
    portmap = PortmapConfig(
        mcp_range=(8676, 8699),
        reserved={8681: "available"},
    )
    assert portmap.mcp_range == (8676, 8699)
    assert 8681 in portmap.reserved


def test_storage_map_config():
    """Test storage map configuration."""
    storage = StorageMapConfig(
        databases={
            "session_buddy": "~/data/session-buddy/session_buddy.db",
            "akosha_hot": "~/data/akosha/hot.db",
        },
        caches={
            "redis": "localhost:6379",
        },
    )
    assert "session_buddy" in storage.databases
    assert "redis" in storage.caches
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_models.py::test_portmap_config -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'bodai.models.config'"

**Step 3: Write the implementation**

`bodai/models/config.py`:

```python
"""Configuration models for Bodai."""

from pydantic import BaseModel, Field


class PortmapConfig(BaseModel):
    """Port allocation configuration."""

    mcp_range: tuple[int, int] = Field(default=(8676, 8699))
    reserved: dict[int, str] = Field(default_factory=dict)


class StorageMapConfig(BaseModel):
    """Storage and cache allocation configuration."""

    databases: dict[str, str] = Field(default_factory=dict)
    caches: dict[str, str] = Field(default_factory=dict)
    storage: dict[str, str] = Field(default_factory=dict)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_models.py -v`
Expected: 5 passed

**Step 5: Commit**

```bash
git add bodai/models/config.py tests/test_models.py
git commit -m "feat: add config models for portmap and storage"
```

______________________________________________________________________

## Phase 2: Config Layer

### Task 5: Create config YAML files

**Files:**

- Create: `config/ecosystem.yaml`
- Create: `config/portmap.yaml`
- Create: `config/storage-map.yaml`

**Step 1: Create ecosystem.yaml**

```yaml
# Bodai Ecosystem Component Registry
# The Orb contains all components of the ecosystem

components:
  mahavishnu:
    name: mahavishnu
    role: orchestrator
    port: 8680
    repo: ~/Projects/mahavishnu
    status: production
    description: Multi-engine workflow orchestration and pool management

  akosha:
    name: akosha
    role: seer
    port: 8682
    repo: ~/Projects/akosha
    status: production
    description: Cross-system intelligence and memory aggregation

  dhruva:
    name: dhruva
    role: curator
    port: 8683
    repo: ~/Projects/dhruva
    status: production
    description: Persistent object storage with ACID properties

  session-buddy:
    name: session-buddy
    role: builder
    port: 8678
    repo: ~/Projects/session-buddy
    status: production
    description: Session lifecycle management and knowledge graphs

  crackerjack:
    name: crackerjack
    role: inspector
    port: 8676
    repo: ~/Projects/crackerjack
    status: production
    description: Quality gates, testing, and CI/CD validation
```

**Step 2: Create portmap.yaml**

```yaml
# Bodai Ecosystem Port Allocation
# MCP servers: 8676-8699

mcp_range:
  start: 8676
  end: 8699

allocations:
  8676: crackerjack    # Inspector
  8678: session-buddy  # Builder
  8680: mahavishnu     # Orchestrator
  8681: available      # (Oneiric MCP absorbed into Dhruva)
  8682: akosha         # Seer
  8683: dhruva         # Curator

reserved:
  8684-8699: future expansion
```

**Step 3: Create storage-map.yaml**

```yaml
# Bodai Ecosystem Storage Map
# Databases, caches, and persistent storage allocations

databases:
  session_buddy:
    path: ~/data/session-buddy/session_buddy.db
    type: duckdb
    description: Session memories and knowledge graph

  akosha_hot:
    path: ~/data/akosha/hot.db
    type: duckdb
    description: Hot tier for recent data (0-7 days)

  akosha_warm:
    path: ~/data/akosha/warm.db
    type: duckdb
    description: Warm tier for historical data (7-90 days)

  dhruva:
    path: ~/data/dhruva/dhruva.db
    type: dhruva
    description: Persistent object storage

caches:
  redis:
    host: localhost
    port: 6379
    description: Shared cache layer

storage:
  akosha_cold:
    backend: s3
    bucket: akosha-cold-data
    description: Cold tier for archival (90+ days)
```

**Step 4: Commit**

```bash
git add config/
git commit -m "feat: add ecosystem config files (YAML)"
```

______________________________________________________________________

### Task 6: Create config loader

**Files:**

- Create: `bodai/core/config.py`
- Create: `tests/test_config.py`

**Step 1: Write the failing test**

`tests/test_config.py`:

```python
"""Tests for config loading."""

import pytest
from pathlib import Path

from bodai.core.config import load_ecosystem, load_portmap, load_storage_map
from bodai.models.ecosystem import Ecosystem


def test_load_ecosystem():
    """Test loading ecosystem from YAML."""
    ecosystem = load_ecosystem()
    assert isinstance(ecosystem, Ecosystem)
    assert len(ecosystem.components) == 5
    assert "mahavishnu" in ecosystem.components


def test_load_portmap():
    """Test loading portmap from YAML."""
    portmap = load_portmap()
    assert portmap.mcp_range == (8676, 8699)
    assert 8681 in portmap.reserved


def test_load_storage_map():
    """Test loading storage map from YAML."""
    storage = load_storage_map()
    assert "session_buddy" in storage.databases
    assert "redis" in storage.caches
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'bodai.core.config'"

**Step 3: Write the implementation**

`bodai/core/config.py`:

```python
"""Configuration loading for Bodai."""

from pathlib import Path

import yaml

from bodai.models.config import PortmapConfig, StorageMapConfig
from bodai.models.ecosystem import Component, Ecosystem

CONFIG_DIR = Path(__file__).parent.parent.parent / "config"


def load_ecosystem() -> Ecosystem:
    """Load ecosystem configuration from YAML."""
    config_path = CONFIG_DIR / "ecosystem.yaml"
    with open(config_path) as f:
        data = yaml.safe_load(f)

    components = {}
    for name, comp_data in data.get("components", {}).items():
        components[name] = Component(**comp_data)

    return Ecosystem(components=components)


def load_portmap() -> PortmapConfig:
    """Load portmap configuration from YAML."""
    config_path = CONFIG_DIR / "portmap.yaml"
    with open(config_path) as f:
        data = yaml.safe_load(f)

    mcp_range = (
        data.get("mcp_range", {}).get("start", 8676),
        data.get("mcp_range", {}).get("end", 8699),
    )

    reserved = {}
    for port, desc in data.get("reserved", {}).items():
        if isinstance(port, int):
            reserved[port] = desc
        elif "-" in str(port):
            # Handle ranges like "8684-8699"
            start, end = map(int, port.split("-"))
            for p in range(start, end + 1):
                reserved[p] = desc

    return PortmapConfig(mcp_range=mcp_range, reserved=reserved)


def load_storage_map() -> StorageMapConfig:
    """Load storage map configuration from YAML."""
    config_path = CONFIG_DIR / "storage-map.yaml"
    with open(config_path) as f:
        data = yaml.safe_load(f)

    databases = {
        name: info.get("path", "")
        for name, info in data.get("databases", {}).items()
    }

    caches = {
        name: f"{info.get('host', 'localhost')}:{info.get('port', 6379)}"
        for name, info in data.get("caches", {}).items()
    }

    storage = {
        name: info.get("bucket", "")
        for name, info in data.get("storage", {}).items()
    }

    return StorageMapConfig(databases=databases, caches=caches, storage=storage)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_config.py -v`
Expected: 3 passed

**Step 5: Commit**

```bash
git add bodai/core/config.py tests/test_config.py
git commit -m "feat: add config loader for YAML files"
```

______________________________________________________________________

## Phase 3: Health Check Layer

### Task 7: Create health check module

**Files:**

- Create: `bodai/core/health.py`
- Create: `tests/test_health.py`

**Step 1: Write the failing test**

`tests/test_health.py`:

```python
"""Tests for health check functionality."""

import pytest

from bodai.core.health import check_port, check_component, check_all, HealthStatus


def test_health_status_enum():
    """Test health status enum values."""
    assert HealthStatus.HEALTHY.value == "healthy"
    assert HealthStatus.UNHEALTHY.value == "unhealthy"
    assert HealthStatus.UNKNOWN.value == "unknown"


def test_check_port_localhost():
    """Test checking a port that should be listening."""
    # This tests the function exists; actual port may not be open
    result = check_port(12345)  # Unlikely port
    assert result in [HealthStatus.HEALTHY, HealthStatus.UNHEALTHY]


def test_check_component_returns_dict():
    """Test check_component returns proper structure."""
    from bodai.core.config import load_ecosystem

    ecosystem = load_ecosystem()
    component = ecosystem.components["mahavishnu"]

    result = check_component(component)
    assert "name" in result
    assert "port" in result
    assert "status" in result
    assert result["name"] == "mahavishnu"


def test_check_all_returns_all_components():
    """Test check_all returns status for all components."""
    results = check_all()
    assert len(results) == 5
    assert all("status" in r for r in results.values())
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_health.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'bodai.core.health'"

**Step 3: Write the implementation**

`bodai/core/health.py`:

```python
"""Health check functionality for ecosystem components."""

import socket
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

from bodai.core.config import load_ecosystem
from bodai.models.ecosystem import Component


class HealthStatus(str, Enum):
    """Health status of a component."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


def check_port(port: int, host: str = "localhost", timeout: float = 1.0) -> HealthStatus:
    """Check if a port is accepting connections."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return HealthStatus.HEALTHY if result == 0 else HealthStatus.UNHEALTHY
    except (socket.error, OSError):
        return HealthStatus.UNHEALTHY


def check_component(component: Component) -> dict:
    """Check health of a single component."""
    status = check_port(component.port)
    return {
        "name": component.name,
        "port": component.port,
        "status": status,
        "role": component.role_display,
        "description": component.description,
    }


def check_all() -> dict[str, dict]:
    """Check health of all ecosystem components in parallel."""
    ecosystem = load_ecosystem()
    results = {}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(check_component, comp): name
            for name, comp in ecosystem.components.items()
        }

        for future in as_completed(futures):
            name = futures[future]
            results[name] = future.result()

    return results
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_health.py -v`
Expected: 4 passed

**Step 5: Commit**

```bash
git add bodai/core/health.py tests/test_health.py
git commit -m "feat: add health check module with parallel checking"
```

______________________________________________________________________

## Phase 4: CLI Layer

### Task 8: Create Typer CLI

**Files:**

- Create: `bodai/cli.py`
- Create: `tests/test_cli.py`

**Step 1: Write the failing test**

`tests/test_cli.py`:

```python
"""Tests for CLI commands."""

from typer.testing import CliRunner

from bodai.cli import app

runner = CliRunner()


def test_cli_help():
    """Test CLI help output."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "bodai" in result.output.lower()


def test_health_command():
    """Test health check command."""
    result = runner.invoke(app, ["health"])
    assert result.exit_code == 0
    # Should show table with components
    assert "mahavishnu" in result.output.lower() or "orchestrator" in result.output.lower()


def test_config_show_command():
    """Test config show command."""
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'bodai.cli'"

**Step 3: Write the implementation**

`bodai/cli.py`:

```python
"""Typer CLI for Bodai."""

import typer
from rich.console import Console
from rich.table import Table

from bodai.core.config import load_ecosystem, load_portmap, load_storage_map
from bodai.core.health import check_all, HealthStatus

app = typer.Typer(
    name="bodai",
    help="The Orb - Ecosystem meta-manager",
    add_completion=False,
)
console = Console()

config_app = typer.Typer(help="Configuration commands")
app.add_typer(config_app, name="config")


@app.command()
def health(
    watch: bool = typer.Option(False, "--watch", "-w", help="Continuous monitoring"),
) -> None:
    """Check health of all ecosystem components."""
    results = check_all()
    _display_health_table(results)


def _display_health_table(results: dict) -> None:
    """Display health results in a Rich table."""
    table = Table(title="Bodai Ecosystem Health")
    table.add_column("Component", style="cyan")
    table.add_column("Port", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Role")

    status_symbols = {
        HealthStatus.HEALTHY: "[green]●[/green]",
        HealthStatus.UNHEALTHY: "[red]○[/red]",
        HealthStatus.UNKNOWN: "[yellow]◆[/yellow]",
    }

    for name, result in sorted(results.items()):
        status = result["status"]
        symbol = status_symbols.get(status, "◆")
        table.add_row(
            name,
            str(result["port"]),
            symbol,
            result["role"],
        )

    console.print(table)

    # Summary
    healthy = sum(1 for r in results.values() if r["status"] == HealthStatus.HEALTHY)
    total = len(results)
    console.print(f"\n  [green]●[/green] healthy   [red]○[/red] unhealthy   [yellow]◆[/yellow] unknown")
    console.print(f"  Summary: {healthy}/{total} healthy")


@app.command()
def start(
    components: list[str] = typer.Argument(None, help="Components to start (default: all)"),
) -> None:
    """Start ecosystem components."""
    # Placeholder - actual implementation requires subprocess management
    if components:
        console.print(f"[yellow]Starting:[/yellow] {', '.join(components)}")
    else:
        console.print("[yellow]Starting all components...[/yellow]")
    console.print("[dim]Implementation pending - use individual component start scripts[/dim]")


@app.command()
def stop(
    components: list[str] = typer.Argument(None, help="Components to stop (default: all)"),
) -> None:
    """Stop ecosystem components."""
    if components:
        console.print(f"[red]Stopping:[/red] {', '.join(components)}")
    else:
        console.print("[red]Stopping all components...[/red]")
    console.print("[dim]Implementation pending - use individual component stop scripts[/dim]")


@app.command()
def restart(
    components: list[str] = typer.Argument(None, help="Components to restart (default: all)"),
) -> None:
    """Restart ecosystem components."""
    if components:
        console.print(f"[yellow]Restarting:[/yellow] {', '.join(components)}")
    else:
        console.print("[yellow]Restarting all components...[/yellow]")
    console.print("[dim]Implementation pending[/dim]")


@app.command()
def status() -> None:
    """Show cached status of ecosystem."""
    console.print("[cyan]Bodai Ecosystem Status[/cyan]")
    health(None)


@app.command()
def dashboard() -> None:
    """Launch TUI health dashboard."""
    console.print("[cyan]Launching dashboard...[/cyan]")
    try:
        from bodai.tui.dashboard import BodaiDashboard
        app = BodaiDashboard()
        app.run()
    except ImportError:
        console.print("[red]TUI not yet implemented[/red]")


@app.command()
def shell() -> None:
    """Launch IPython admin shell."""
    console.print("[cyan]Launching IPython shell...[/cyan]")
    try:
        from bodai.admin.shell import launch_shell
        launch_shell()
    except ImportError:
        console.print("[red]Shell not yet implemented[/red]")


@config_app.command("show")
def config_show() -> None:
    """Display current configuration."""
    console.print("[cyan]Ecosystem Configuration[/cyan]\n")

    ecosystem = load_ecosystem()
    table = Table(title="Components")
    table.add_column("Name")
    table.add_column("Role")
    table.add_column("Port")
    table.add_column("Status")

    for name, comp in ecosystem.components.items():
        table.add_row(name, comp.role_display, str(comp.port), comp.status.value)

    console.print(table)


@config_app.command("validate")
def config_validate() -> None:
    """Validate all configuration files."""
    console.print("[cyan]Validating configuration...[/cyan]")

    try:
        ecosystem = load_ecosystem()
        console.print(f"[green]✓[/green] ecosystem.yaml: {len(ecosystem.components)} components")
    except Exception as e:
        console.print(f"[red]✗[/red] ecosystem.yaml: {e}")

    try:
        portmap = load_portmap()
        console.print(f"[green]✓[/green] portmap.yaml: range {portmap.mcp_range}")
    except Exception as e:
        console.print(f"[red]✗[/red] portmap.yaml: {e}")

    try:
        storage = load_storage_map()
        console.print(f"[green]✓[/green] storage-map.yaml: {len(storage.databases)} databases")
    except Exception as e:
        console.print(f"[red]✗[/red] storage-map.yaml: {e}")


if __name__ == "__main__":
    app()
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli.py -v`
Expected: 3 passed

**Step 5: Commit**

```bash
git add bodai/cli.py tests/test_cli.py
git commit -m "feat: add Typer CLI with health, start, stop, config commands"
```

______________________________________________________________________

## Phase 5: TUI Dashboard

### Task 9: Create Textual TUI dashboard

**Files:**

- Create: `bodai/tui/dashboard.py`
- Create: `bodai/tui/dashboard.css`

**Step 1: Create dashboard implementation**

`bodai/tui/dashboard.py`:

```python
"""Textual TUI dashboard for Bodai ecosystem health."""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static, Label
from textual.binding import Binding
from textual.reactive import reactive

from bodai.core.health import check_all, HealthStatus


class ComponentWidget(Static):
    """Widget displaying a single component's health."""

    def __init__(self, name: str, data: dict) -> None:
        super().__init__()
        self.name = name
        self.data = data

    def compose(self) -> ComposeResult:
        status = self.data["status"]
        status_color = {
            HealthStatus.HEALTHY: "green",
            HealthStatus.UNHEALTHY: "red",
            HealthStatus.UNKNOWN: "yellow",
        }.get(status, "yellow")

        symbol = "●" if status == HealthStatus.HEALTHY else "○"

        yield Label(
            f"[{status_color}]{symbol}[/{status_color}] {self.name}",
            classes="component-name",
        )
        yield Label(
            f"  [{status_color}]{self.data['role']}[/{status_color}]  Port {self.data['port']}",
            classes="component-details",
        )


class ComponentList(Container):
    """Container for all component widgets."""

    def __init__(self) -> None:
        super().__init__()
        self._load_components()

    def _load_components(self) -> None:
        """Load component health data."""
        self.results = check_all()

    def compose(self) -> ComposeResult:
        for name, data in sorted(self.results.items()):
            yield ComponentWidget(name, data)

    def refresh_health(self) -> None:
        """Refresh health data."""
        self._load_components()
        # Re-render
        for child in self.query(ComponentWidget):
            child.remove()
        for name, data in sorted(self.results.items()):
            self.mount(ComponentWidget(name, data))


class BodaiDashboard(App):
    """Bodai ecosystem health dashboard."""

    CSS_PATH = "dashboard.css"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
    ]

    TITLE = "Bodai Ecosystem Dashboard"

    def compose(self) -> ComposeResult:
        yield Header()
        yield ComponentList()
        yield Footer()

    def action_refresh(self) -> None:
        """Refresh health data."""
        component_list = self.query_one(ComponentList)
        component_list.refresh_health()
        self.notify("Health data refreshed")


if __name__ == "__main__":
    app = BodaiDashboard()
    app.run()
```

**Step 2: Create dashboard CSS**

`bodai/tui/dashboard.css`:

```css
Screen {
    background: $surface;
}

ComponentList {
    layout: vertical;
    padding: 1 2;
    overflow-y: auto;
}

ComponentWidget {
    layout: vertical;
    margin: 1 0;
    padding: 1;
    background: $panel;
    border: solid $primary;
}

.component-name {
    text-style: bold;
}

.component-details {
    color: $text-muted;
    margin-left: 2;
}

Header {
    background: $primary;
    color: $text-on-primary;
}

Footer {
    background: $panel;
}
```

**Step 3: Verify import**

Run: `python -c "from bodai.tui.dashboard import BodaiDashboard; print('OK')"`
Expected: `OK`

**Step 4: Commit**

```bash
git add bodai/tui/
git commit -m "feat: add Textual TUI health dashboard"
```

______________________________________________________________________

## Phase 6: IPython Admin Shell

### Task 10: Create IPython admin shell

**Files:**

- Create: `bodai/admin/shell.py`

**Step 1: Create shell implementation**

`bodai/admin/shell.py`:

```python
"""IPython admin shell for Bodai ecosystem management."""

from rich import print

from bodai.core.config import load_ecosystem, load_portmap, load_storage_map
from bodai.core.health import check_all, check_component
from bodai.models.ecosystem import Component, Ecosystem


def launch_shell() -> None:
    """Launch IPython with Bodai context pre-loaded."""
    # Load configuration
    ecosystem = load_ecosystem()
    portmap = load_portmap()
    storage_map = load_storage_map()

    # Welcome banner
    print("[bold cyan]═══════════════════════════════════════[/bold cyan]")
    print("[bold cyan]       Bodai Admin Shell[/bold cyan]")
    print("[bold cyan]═══════════════════════════════════════[/bold cyan]")
    print()
    print(f"  [green]Ecosystem:[/green] {len(ecosystem.components)} components")
    print(f"  [green]Port Range:[/green] {portmap.mcp_range[0]}-{portmap.mcp_range[1]}")
    print()

    # Pre-loaded namespace
    user_ns = {
        # Config objects
        "ecosystem": ecosystem,
        "portmap": portmap,
        "storage_map": storage_map,
        # Config functions
        "load_ecosystem": load_ecosystem,
        "load_portmap": load_portmap,
        "load_storage_map": load_storage_map,
        # Health functions
        "check_all": check_all,
        "check_component": check_component,
        # Models
        "Component": Component,
        "Ecosystem": Ecosystem,
        # Quick access to components
        **{name: comp for name, comp in ecosystem.components.items()},
    }

    # Print available variables
    print("[yellow]Pre-loaded:[/yellow]")
    print("  ecosystem, portmap, storage_map")
    print("  check_all(), check_component(comp)")
    print()
    print("[dim]Components available as variables:[/dim]")
    comp_names = ", ".join(ecosystem.components.keys())
    print(f"  {comp_names}")
    print()

    # Launch IPython
    from IPython import start_ipython
    from IPython.terminal.interactiveshell import TerminalInteractiveShell

    # Configure IPython
    TerminalInteractiveShell.autoindent = True

    start_ipython(argv=[], user_ns=user_ns)


if __name__ == "__main__":
    launch_shell()
```

**Step 2: Verify import**

Run: `python -c "from bodai.admin.shell import launch_shell; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add bodai/admin/shell.py
git commit -m "feat: add IPython admin shell with pre-loaded context"
```

______________________________________________________________________

## Phase 7: Documentation

### Task 11: Create README.md

**Files:**

- Modify: `README.md`

**Step 1: Write README**

````markdown
# Bodai - The Orb

Meta-project for the Bodai ecosystem. Central hub for understanding and managing the interconnected components of the AI-assisted development environment.

## Ecosystem Components

| Component | Role | Port | Description |
|-----------|------|------|-------------|
| **Mahavishnu** | The Orchestrator | 8680 | Multi-engine workflow orchestration |
| **Akosha** | The Seer | 8682 | Cross-system intelligence |
| **Dhruva** | The Curator | 8683 | Persistent object storage |
| **Session-Buddy** | The Builder | 8678 | Session management |
| **Crackerjack** | The Inspector | 8676 | Quality gates and CI/CD |

## Installation

```bash
uv sync
````

## Commands

```bash
bodai health                    # Check all components
bodai health --watch            # Continuous monitoring
bodai start [components...]     # Start components
bodai stop [components...]      # Stop components
bodai restart [components...]   # Restart components
bodai dashboard                 # Launch TUI dashboard
bodai shell                     # Launch IPython admin shell
bodai config show               # Show configuration
bodai config validate           # Validate config files
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed system design.

## The Orb Metaphor

Bodai (The Orb) is the container that holds and describes the entire ecosystem. Like an orb that reflects and contains all things, Bodai provides:

- **Configuration**: Central registry of all components
- **Documentation**: Explains how the ecosystem works
- **Operations**: Tools to manage ecosystem health

## Development

```bash
# Run tests
pytest

# Run all quality checks
crackerjack run
```

````

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add comprehensive README"
````

______________________________________________________________________

### Task 12: Create CLAUDE.md

**Files:**

- Create: `CLAUDE.md`

**Step 1: Write CLAUDE.md**

````markdown
# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Bodai (The Orb) is the meta-project for the Bodai ecosystem. It provides configuration, documentation, and operational tooling for managing the interconnected components.

## Ecosystem Components

| Component | Role | Port |
|-----------|------|------|
| Mahavishnu | Orchestrator | 8680 |
| Akosha | Seer | 8682 |
| Dhruva | Curator | 8683 |
| Session-Buddy | Builder | 8678 |
| Crackerjack | Inspector | 8676 |

## Development Commands

### Installation

```bash
uv sync --group dev
````

### Testing

```bash
pytest                           # Run all tests
pytest tests/test_health.py      # Run specific test file
pytest --cov=bodai               # With coverage
```

### Code Quality

```bash
crackerjack lint                 # Lint and format
crackerjack typecheck            # Type checking
crackerjack security             # Security scan
```

### Running CLI

```bash
python -m bodai.cli health
python -m bodai.cli dashboard
python -m bodai.cli shell
```

## Architecture

Three layers:

1. **Config** (`bodai/core/config.py`) - Load YAML configs via Oneiric pattern
1. **Models** (`bodai/models/`) - Pydantic models for ecosystem, portmap, storage
1. **Operations** (`bodai/cli.py`, `bodai/core/health.py`) - CLI, health checks, TUI

## Key Patterns

- **Pydantic models** for all configuration with validation
- **Typer** for CLI with Rich output
- **Textual** for TUI dashboard
- **Concurrent health checks** via ThreadPoolExecutor

## Configuration Files

- `config/ecosystem.yaml` - Component registry
- `config/portmap.yaml` - Port allocations
- `config/storage-map.yaml` - DB and cache mappings

````

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md for development guidance"
````

______________________________________________________________________

### Task 13: Create documentation files

**Files:**

- Create: `docs/architecture.md`
- Create: `docs/roles.md`
- Create: `docs/symbiosis.md`
- Create: `docs/portmap.md`

**Step 1: Create architecture.md**

````markdown
# Bodai Ecosystem Architecture

## System Overview

```mermaid
graph TB
    subgraph "The Orb - Bodai"
        B[Bodai Meta-Project]
        B --> C[Config]
        B --> D[Docs]
        B --> O[Operations]
    end

    subgraph "Ecosystem Components"
        M[Mahavishnu<br/>Orchestrator:8680]
        A[Akosha<br/>Seer:8682]
        Dh[Dhruva<br/>Curator:8683]
        SB[Session-Buddy<br/>Builder:8678]
        CJ[Crackerjack<br/>Inspector:8676]
    end

    O --> |health/start/stop| M
    O --> |health/start/stop| A
    O --> |health/start/stop| Dh
    O --> |health/start/stop| SB
    O --> |health/start/stop| CJ

    M --> |orchestrates| A
    M --> |orchestrates| SB
    SB --> |uploads to| A
    CJ --> |validates| M
    CJ --> |validates| A
    Dh --> |stores for| M
    Dh --> |stores for| A
````

## Component Boundaries

Each component owns its domain:

| Component | Owns |
|-----------|------|
| **Mahavishnu** | Workflow definitions, pool management, scheduling |
| **Akosha** | Cross-system memory, embeddings, knowledge graphs |
| **Dhruva** | Object persistence, ACID transactions, caching |
| **Session-Buddy** | Session lifecycle, local memory, reflections |
| **Crackerjack** | Quality rules, test execution, linting |

## Data Flow

1. **Session → Akosha**: Session-Buddy uploads memories to cloud; Akosha ingests
1. **Mahavishnu → All**: Orchestrates workflows across components
1. **Crackerjack → All**: Validates quality on all code changes
1. **Dhruva → All**: Provides persistent storage backends

````

**Step 2: Create roles.md**

```markdown
# Ecosystem Roles

Each component has a distinct role in the ecosystem.

## The Orchestrator (Mahavishnu)

**Port:** 8680

**Responsibilities:**
- Multi-engine workflow coordination
- Pool management for horizontal scaling
- Task scheduling and distribution
- WebSocket infrastructure for real-time monitoring

## The Seer (Akosha)

**Port:** 8682

**Responsibilities:**
- Cross-system intelligence aggregation
- Vector embeddings (100M-1B scale)
- Pattern recognition across 100-10,000 systems
- Three-tier storage: Hot (0-7d), Warm (7-90d), Cold (90+d)

## The Curator (Dhruva)

**Port:** 8683

**Responsibilities:**
- Persistent object storage with ACID guarantees
- Transaction management
- Aggressive caching for read-heavy workloads
- Multiple serialization backends (msgspec, etc.)

## The Builder (Session-Buddy)

**Port:** 8678

**Responsibilities:**
- Session lifecycle management
- Knowledge graph construction
- Memory collection and reflection storage
- Bridge between sessions and ecosystem memory

## The Inspector (Crackerjack)

**Port:** 8676

**Responsibilities:**
- Quality gates and linting
- Test execution and coverage
- Security scanning
- CI/CD integration

## The Resolver (Oneiric)

**Status:** Library (no MCP server)

**Responsibilities:**
- Universal component resolution
- Hot-swapping with health checks
- Multi-domain support (adapters, services, tasks)
````

**Step 3: Create symbiosis.md**

```markdown
# Ecosystem Symbiosis

How components work together.

## Session-Buddy → Akosha

Session-Buddy collects session memories locally, then uploads to cloud storage. Akosha pulls from cloud and aggregates across all systems.

```

Session-Buddy → S3://session-buddy-memories/ → Akosha Worker → Hot Store

```

## Mahavishnu → All

Mahavishnu orchestrates workflows across the ecosystem:

- Schedules Akosha ingestion jobs
- Coordinates Session-Buddy sync
- Triggers Crackerjack quality gates
- Manages Dhruva backup schedules

## Crackerjack → All

Quality validation for all components:

- Pre-commit hooks for code quality
- Test execution on all changes
- Security scanning for vulnerabilities
- Coverage enforcement (85%+)

## Dhruva → All

Storage backbone:

- Session-Buddy: DuckDB via Oneiric adapters
- Akosha: Hot/Warm DuckDB + Cold Parquet
- Mahavishnu: Workflow state persistence
- Crackerjack: Coverage and quality metrics

## Oneiric → All

Configuration resolution:

- All components use Oneiric for layered config loading
- Hot-swapping of adapters without restart
- Remote manifest delivery for distributed deployments
```

**Step 4: Create portmap.md**

```markdown
# Port Allocation

## MCP Server Range: 8676-8699

| Port | Component | Role |
|------|-----------|------|
| 8676 | Crackerjack | Inspector |
| 8678 | Session-Buddy | Builder |
| 8680 | Mahavishnu | Orchestrator |
| 8681 | *Available* | (Oneiric absorbed into Dhruva) |
| 8682 | Akosha | Seer |
| 8683 | Dhruva | Curator |
| 8684-8699 | *Reserved* | Future expansion |

## Rationale

- **8676-8699 range**: Easy to remember, grouped together
- **Gaps intentionally left**: Room for new components
- **Ascending by role precedence**: Inspector → Builder → Orchestrator → Seer → Curator
```

**Step 5: Commit**

```bash
git add docs/
git commit -m "docs: add architecture, roles, symbiosis, and portmap documentation"
```

______________________________________________________________________

## Phase 8: Final Verification

### Task 14: Run full test suite

**Step 1: Run all tests**

Run: `pytest tests/ -v --cov=bodai`
Expected: All tests pass, coverage >80%

**Step 2: Run CLI smoke test**

Run: `python -m bodai.cli --help`
Expected: Help output displayed

Run: `python -m bodai.cli health`
Expected: Health table with 5 components

**Step 3: Final commit**

```bash
git add -A
git commit -m "chore: final verification and cleanup"
```

______________________________________________________________________

## Summary

**14 tasks** organized into 8 phases:

1. **Project Setup** - pyproject.toml, package structure, models
1. **Config Layer** - YAML files, config loader
1. **Health Check** - Port checking, component health
1. **CLI Layer** - Typer commands, Rich output
1. **TUI Dashboard** - Textual interface
1. **IPython Shell** - Admin shell with context
1. **Documentation** - README, CLAUDE.md, docs
1. **Verification** - Full test suite
