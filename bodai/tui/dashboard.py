"""Textual TUI dashboard for Bodai ecosystem health."""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static, Label
from textual.binding import Binding

from bodai.core.health import check_all, HealthStatus


class ComponentWidget(Static):
    """Widget displaying a single component's health."""

    def __init__(self, component_name: str, data: dict) -> None:
        super().__init__()
        self.component_name = component_name
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
            f"[{status_color}]{symbol}[/{status_color}] {self.component_name}",
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
        self.results = check_all()

    def compose(self) -> ComposeResult:
        for name, data in sorted(self.results.items()):
            yield ComponentWidget(name, data)

    def refresh_health(self) -> None:
        self._load_components()
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
        component_list = self.query_one(ComponentList)
        component_list.refresh_health()
        self.notify("Health data refreshed")


if __name__ == "__main__":
    app = BodaiDashboard()
    app.run()
