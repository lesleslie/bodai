"""Typer CLI for Bodai."""

import typer
from rich.console import Console
from rich.table import Table

from bodai.core.config import load_ecosystem, load_portmap, load_storage_map
from bodai.core.health import HealthStatus, check_all

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
        HealthStatus.HEALTHY: "[green]*[/green]",
        HealthStatus.UNHEALTHY: "[red]o[/red]",
        HealthStatus.UNKNOWN: "[yellow]+[/yellow]",
    }

    for name, result in sorted(results.items()):
        status = result["status"]
        symbol = status_symbols.get(status, "+")
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
    console.print(f"\n  [green]*[/green] healthy   [red]o[/red] unhealthy   [yellow]+[/yellow] unknown")
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
        console.print(f"[green]+[/green] ecosystem.yaml: {len(ecosystem.components)} components")
    except Exception as e:
        console.print(f"[red]-[/red] ecosystem.yaml: {e}")

    try:
        portmap = load_portmap()
        console.print(f"[green]+[/green] portmap.yaml: range {portmap.mcp_range}")
    except Exception as e:
        console.print(f"[red]-[/red] portmap.yaml: {e}")

    try:
        storage = load_storage_map()
        console.print(f"[green]+[/green] storage-map.yaml: {len(storage.databases)} databases")
    except Exception as e:
        console.print(f"[red]-[/red] storage-map.yaml: {e}")


if __name__ == "__main__":
    app()
