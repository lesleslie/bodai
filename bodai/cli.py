"""Typer CLI for Bodai."""

import asyncio
import importlib.metadata
import sys
import time

import typer
from rich.console import Console
from rich.table import Table

from bodai.core.config import load_ecosystem, load_portmap, load_storage_map
from bodai.core.health import HealthStatus, check_all
from bodai.core.operations import EcosystemOperations

app = typer.Typer(
    name="bodai",
    help="The Orb - Ecosystem meta-manager",
    add_completion=False,
)
console = Console()

config_app = typer.Typer(help="Configuration commands")
app.add_typer(config_app, name="config")

# Entry-point group for bodai sub-apps. Spec §5.1: any package can register a
# Typer instance via [project.entry-points."bodai.apps"] in pyproject.toml.
_BODAI_APPS_GROUP = "bodai.apps"


def _iter_bodai_entry_points() -> list:
    """Return entry points in the ``bodai.apps`` group, across Python versions.

    On Python 3.10+ we use the keyword argument. On older interpreters we fall
    back to the dict form (Risk Row 22). Bodai requires Python 3.14 so the
    fallback is purely defensive; the wider ecosystem still has a few 3.9
    call-sites that import ``bodai.cli``.
    """
    if sys.version_info >= (3, 10):  # noqa: UP036 (Risk Row 22 defensive)
        eps = importlib.metadata.entry_points(group=_BODAI_APPS_GROUP)
    else:
        all_eps = importlib.metadata.entry_points()
        eps = all_eps.get(_BODAI_APPS_GROUP, [])
    return list(eps)


def _discover_apps(app: typer.Typer) -> None:
    """Discover and attach ``bodai.apps`` entry points to ``app``.

    Walks :func:`importlib.metadata.entry_points` for the ``bodai.apps``
    group and attaches each registered Typer sub-app via ``app.add_typer``.
    Per-app import failures are caught narrowly (Risk Row 7) and emit a
    yellow warning via :data:`console`; the broken entry point is skipped so
    a single misbehaving plugin cannot block the rest of the CLI surface.

    Risk Row 21: this helper is invoked lazily from
    ``if __name__ == "__main__":``. Importing ``bodai.cli`` does NOT trigger
    entry-point discovery, so test environments stay fast and side-effect
    free.
    """
    try:
        eps = _iter_bodai_entry_points()
    except ImportError, ModuleNotFoundError:
        console.print("[yellow]no bodai.apps registered[/yellow]")
        return
    except Exception as exc:  # narrow: metadata backend failures only
        console.print(f"[yellow]entry-point lookup failed: {exc}[/yellow]")
        return

    if not eps:
        console.print("[yellow]no bodai.apps registered[/yellow]")
        return

    for ep in eps:
        try:
            sub_app = ep.load()
        except (ImportError, ModuleNotFoundError) as exc:
            console.print(
                f"[yellow]skipping bodai.app '{ep.name}': import error {exc}[/yellow]"
            )
            continue
        except Exception as exc:
            console.print(
                f"[yellow]skipping bodai.app '{ep.name}': load error {exc}[/yellow]"
            )
            continue

        if not isinstance(sub_app, typer.Typer):
            console.print(
                f"[yellow]skipping bodai.app '{ep.name}': "
                f"not a Typer instance ({type(sub_app).__name__})[/yellow]"
            )
            continue

        try:
            app.add_typer(sub_app, name=ep.name)
        except Exception as exc:
            console.print(
                f"[yellow]failed to attach bodai.app '{ep.name}': {exc}[/yellow]"
            )


def _health_table(results: dict) -> Table:
    """Build health table."""
    table = Table(title="Bodai Ecosystem Health")
    table.add_column("Component", style="cyan")
    table.add_column("Host")
    table.add_column("Port", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Role")

    status_symbols = {
        HealthStatus.HEALTHY: "[green]*[/green]",
        HealthStatus.UNHEALTHY: "[red]o[/red]",
        HealthStatus.UNKNOWN: "[yellow]+[/yellow]",
    }

    for name, result in sorted(results.items()):
        status = result["status"]
        symbol = status_symbols.get(status, "+")
        table.add_row(
            name,
            str(result.get("host", "localhost")),
            str(result["port"]),
            symbol,
            result["role"],
        )

    return table


def _display_health_table(results: dict) -> None:
    """Display health results in a Rich table."""
    console.print(_health_table(results))

    healthy = sum(1 for r in results.values() if r["status"] == HealthStatus.HEALTHY)
    total = len(results)
    console.print(
        "\n  [green]*[/green] healthy   [red]o[/red] unhealthy   "
        "[yellow]+[/yellow] unknown"
    )
    console.print(f"  Summary: {healthy}/{total} healthy")


@app.command()
def health(
    watch: bool = typer.Option(False, "--watch", "-w", help="Continuous monitoring"),
    interval: float = typer.Option(
        2.0, "--interval", min=0.5, help="Refresh interval (s)"
    ),
) -> None:
    """Check health of all ecosystem components."""
    if not watch:
        _display_health_table(check_all())
        return

    while True:
        console.clear()
        _display_health_table(check_all())
        console.print("\n[dim]Press Ctrl+C to stop watching[/dim]")
        time.sleep(interval)


@app.command()
def start(
    components: list[str] = typer.Argument(
        None, help="Components to start (default: all)"
    ),
) -> None:
    """Start ecosystem components."""

    async def _run() -> dict[str, bool]:
        ops = EcosystemOperations()
        if components:
            return {name: await ops.start_component(name) for name in components}
        return await ops.start_all()

    results = asyncio.run(_run())
    for name, ok in results.items():
        marker = "[green]+[/green]" if ok else "[red]-[/red]"
        console.print(f"{marker} {name}")


@app.command()
def stop(
    components: list[str] = typer.Argument(
        None, help="Components to stop (default: all)"
    ),
    timeout: float = typer.Option(
        30.0, "--timeout", min=1.0, help="Shutdown timeout (s)"
    ),
) -> None:
    """Stop ecosystem components."""

    async def _run() -> dict[str, bool]:
        ops = EcosystemOperations()
        if components:
            return {
                name: await ops.stop_component(name, timeout=timeout)
                for name in components
            }
        return await ops.stop_all(timeout=timeout)

    results = asyncio.run(_run())
    for name, ok in results.items():
        marker = "[green]+[/green]" if ok else "[red]-[/red]"
        console.print(f"{marker} {name}")


@app.command()
def restart(
    components: list[str] = typer.Argument(
        None, help="Components to restart (default: all)"
    ),
    timeout: float = typer.Option(
        30.0, "--timeout", min=1.0, help="Shutdown timeout (s)"
    ),
) -> None:
    """Restart ecosystem components."""

    async def _run() -> dict[str, bool]:
        ops = EcosystemOperations()
        targets = components or list(ops.components.keys())
        return {
            name: await ops.restart_component(name, timeout=timeout) for name in targets
        }

    results = asyncio.run(_run())
    for name, ok in results.items():
        marker = "[green]+[/green]" if ok else "[red]-[/red]"
        console.print(f"{marker} {name}")


@app.command()
def status() -> None:
    """Show current ecosystem health status."""
    _display_health_table(check_all())


@app.command()
def dashboard() -> None:
    """Launch TUI health dashboard."""
    console.print("[cyan]Launching dashboard...[/cyan]")
    try:
        from bodai.tui.dashboard import BodaiDashboard

        tui_app = BodaiDashboard()
        tui_app.run()
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
        console.print(
            f"[green]+[/green] ecosystem.yaml: {len(ecosystem.components)} components"
        )
    except Exception as e:
        console.print(f"[red]-[/red] ecosystem.yaml: {e}")

    try:
        portmap = load_portmap()
        console.print(f"[green]+[/green] portmap.yaml: range {portmap.mcp_range}")
    except Exception as e:
        console.print(f"[red]-[/red] portmap.yaml: {e}")

    try:
        storage = load_storage_map()
        console.print(
            f"[green]+[/green] storage-map.yaml: {len(storage.databases)} databases"
        )
    except Exception as e:
        console.print(f"[red]-[/red] storage-map.yaml: {e}")


@app.command()
def version() -> None:
    """Show installed bodai.apps entry-points and their distribution versions.

    Walks the ``bodai.apps`` entry-point group and prints a two-column Rich
    table of ``{app name, distribution version}``. Distribution version is
    resolved via :func:`importlib.metadata.version` keyed on
    ``entry_point.dist.name``; a dash is rendered when the dist metadata is
    unavailable so the table never crashes on partial installs.
    """
    eps = _iter_bodai_entry_points()
    if not eps:
        console.print("[yellow]no bodai.apps registered[/yellow]")
        return

    table = Table(title="Installed bodai.apps")
    table.add_column("App", style="cyan")
    table.add_column("Version", style="magenta")

    for ep in eps:
        dist_name = getattr(getattr(ep, "dist", None), "name", None) or ep.name
        try:
            ver = importlib.metadata.version(dist_name)
        except ImportError, ModuleNotFoundError:
            ver = "-"
        except Exception:
            ver = "-"
        table.add_row(ep.name, ver)

    console.print(table)


@app.command()
def apps() -> None:
    """List registered bodai.apps entry-point names + their target module paths.

    Each row reports the entry-point ``name`` and the dotted module path the
    plugin's Typer instance is loaded from. Useful for operator diagnostics
    ("which apps have I installed?") and for confirming the entry-point
    group is wired correctly.
    """
    eps = _iter_bodai_entry_points()
    if not eps:
        console.print("[yellow]no bodai.apps registered[/yellow]")
        return

    table = Table(title="Registered bodai.apps")
    table.add_column("App", style="cyan")
    table.add_column("Module", style="magenta")

    for ep in eps:
        # ep.value holds the "<module>:<attr>" string set in pyproject.toml.
        table.add_row(ep.name, str(ep.value))

    console.print(table)


if __name__ == "__main__":
    _discover_apps(app)
    app()
