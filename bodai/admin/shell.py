"""IPython admin shell for Bodai ecosystem management."""

from rich import print as rprint

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
    rprint("[bold cyan]═══════════════════════════════════════[/bold cyan]")
    rprint("[bold cyan]       Bodai Admin Shell[/bold cyan]")
    rprint("[bold cyan]═══════════════════════════════════════[/bold cyan]")
    rprint()
    rprint(f"  [green]Ecosystem:[/green] {len(ecosystem.components)} components")
    rprint(
        f"  [green]Port Range:[/green] {portmap.mcp_range[0]}-{portmap.mcp_range[1]}"
    )
    rprint()

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
        **dict(ecosystem.components.items()),
    }

    # Print available variables
    rprint("[yellow]Pre-loaded:[/yellow]")
    rprint("  ecosystem, portmap, storage_map")
    rprint("  check_all(), check_component(comp)")
    rprint()
    rprint("[dim]Components available as variables:[/dim]")
    comp_names = ", ".join(ecosystem.components.keys())
    rprint(f"  {comp_names}")
    rprint()

    # Launch IPython
    from IPython import start_ipython
    from IPython.terminal.interactiveshell import TerminalInteractiveShell

    TerminalInteractiveShell.autoindent = True  # ty: ignore[invalid-assignment]

    start_ipython(argv=[], user_ns=user_ns)


if __name__ == "__main__":
    launch_shell()
