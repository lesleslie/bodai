"""Typer CLI for Bodai."""

import asyncio
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
    interval: float = typer.Option(2.0, "--interval", min=0.5, help="Refresh interval (s)"),
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
    components: list[str] = typer.Argument(None, help="Components to start (default: all)"),
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
    components: list[str] = typer.Argument(None, help="Components to stop (default: all)"),
    timeout: float = typer.Option(30.0, "--timeout", min=1.0, help="Shutdown timeout (s)"),
) -> None:
    """Stop ecosystem components."""

    async def _run() -> dict[str, bool]:
        ops = EcosystemOperations()
        if components:
            return {name: await ops.stop_component(name, timeout=timeout) for name in components}
        return await ops.stop_all(timeout=timeout)

    results = asyncio.run(_run())
    for name, ok in results.items():
        marker = "[green]+[/green]" if ok else "[red]-[/red]"
        console.print(f"{marker} {name}")


@app.command()
def restart(
    components: list[str] = typer.Argument(None, help="Components to restart (default: all)"),
    timeout: float = typer.Option(30.0, "--timeout", min=1.0, help="Shutdown timeout (s)"),
) -> None:
    """Restart ecosystem components."""

    async def _run() -> dict[str, bool]:
        ops = EcosystemOperations()
        targets = components or list(ops.components.keys())
        return {name: await ops.restart_component(name, timeout=timeout) for name in targets}

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


if __name__ == "__main__":
    app()
