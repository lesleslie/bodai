"""Guard against drift between portmap.yaml and the ports repos actually bind.

portmap.yaml is a registry, not a mandate: a repo's own settings/*.yaml
decides what it binds. Before Plan 0b, portmap.yaml was wrong about six
allocations — it assigned css-mcp to 3049 while css-mcp bound 3050, assigned
spline-mcp to 3050 while spline bound 3052, and omitted penpot-api-mcp,
mdinject, and akosha's mcp_port entirely. A collision would have surfaced
only as a bind failure at runtime.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

BODAI_ROOT = Path(__file__).resolve().parents[1]
PROJECTS_ROOT = BODAI_ROOT.parent
PORTMAP_PATH = BODAI_ROOT / "config" / "portmap.yaml"
ECOSYSTEM_PATH = BODAI_ROOT / "config" / "ecosystem.yaml"

SKIP_DIRS = {"ARCHIVED", "BACKUP", "SCRATCH", "sites"}
PORT_LINE = re.compile(r"^[a-z_]*port:\s*(\d{4})\s*$", re.MULTILINE)


def _load(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return yaml.safe_load(handle)


def _portmap_allocations() -> dict[int, str]:
    """Port -> component name, excluding the 'available' placeholder rows."""
    raw = _load(PORTMAP_PATH).get("allocations", {})
    return {
        int(port): name
        for port, name in raw.items()
        if isinstance(name, str) and name != "available"
    }


def _repo_declared_ports() -> dict[int, set[str]]:
    """Port -> set of repo names declaring it in their own settings/*.yaml."""
    found: dict[int, set[str]] = {}
    for repo_dir in sorted(PROJECTS_ROOT.iterdir()):
        if not repo_dir.is_dir() or repo_dir.name in SKIP_DIRS:
            continue
        if repo_dir.name.startswith("."):
            continue
        settings_dir = repo_dir / "settings"
        if not settings_dir.is_dir():
            continue
        for settings_file in settings_dir.glob("*.yaml"):
            for match in PORT_LINE.finditer(settings_file.read_text()):
                found.setdefault(int(match.group(1)), set()).add(repo_dir.name)
    return found


class TestPortmapMatchesReality:
    """portmap.yaml must agree with what repos declare."""

    def test_no_portmap_entry_contradicts_a_repo(self) -> None:
        """If portmap says port P belongs to A but repo B declares P, that is a
        contradiction the registry must resolve in the repo's favour."""
        allocations = _portmap_allocations()
        declared = _repo_declared_ports()
        contradictions = {
            port: {"portmap": allocations[port], "declared_by": sorted(repos)}
            for port, repos in declared.items()
            if port in allocations and allocations[port] not in repos
        }
        assert contradictions == {}, f"portmap contradicts repos: {contradictions}"

    def test_every_declared_port_is_in_portmap(self) -> None:
        """A repo binding an unregistered port can collide with a future
        allocation without anything noticing."""
        allocations = _portmap_allocations()
        declared = _repo_declared_ports()
        unregistered = {
            port: sorted(repos)
            for port, repos in declared.items()
            if port not in allocations
        }
        assert unregistered == {}, f"declared but not in portmap: {unregistered}"


NEW_SERVER_PORTS = {
    3054: "archive-org-mcp",
    3055: "medium-mcp",
    3056: "scapy-mcp",
}


class TestEcosystemComponentPaths:
    """Every declared component must point at a directory that exists."""

    def test_no_dangling_component_repo(self) -> None:
        components = _load(ECOSYSTEM_PATH).get("components", {})
        dangling = {
            name: spec["repo"]
            for name, spec in components.items()
            if "repo" in spec
            and not Path(str(spec["repo"]).replace("~", str(Path.home()))).is_dir()
        }
        assert dangling == {}, f"components with missing repos: {dangling}"

    def test_dhara_replaces_druva(self) -> None:
        components = _load(ECOSYSTEM_PATH).get("components", {})
        assert "druva" not in components, "druva was renamed to dhara"
        assert "dhara" in components
        assert components["dhara"]["port"] == 8683

    def test_n8n_mcp_is_not_an_active_component(self) -> None:
        """~/Projects/n8n-mcp does not exist. The entry is commented out
        pending a consumer audit rather than deleted."""
        components = _load(ECOSYSTEM_PATH).get("components", {})
        assert "n8n-mcp" not in components

    @pytest.mark.parametrize(("port", "name"), sorted(NEW_SERVER_PORTS.items()))
    def test_new_server_component_declared(self, port: int, name: str) -> None:
        components = _load(ECOSYSTEM_PATH).get("components", {})
        assert name in components
        assert components[name]["port"] == port


class TestNewServerPorts:
    """The three new MCP servers must have registered, non-colliding ports."""

    @pytest.mark.parametrize(("port", "name"), sorted(NEW_SERVER_PORTS.items()))
    def test_new_server_port_allocated(self, port: int, name: str) -> None:
        assert _portmap_allocations().get(port) == name

    def test_new_server_ports_are_unique(self) -> None:
        allocations = _portmap_allocations()
        for port, name in NEW_SERVER_PORTS.items():
            others = {p: n for p, n in allocations.items() if p != port and n == name}
            assert others == {}, f"{name} also allocated at {others}"

    def test_reserved_range_excludes_allocated_ports(self) -> None:
        """A port cannot be both allocated and reserved for future expansion."""
        reserved = _load(PORTMAP_PATH).get("reserved", {})
        allocated = set(_portmap_allocations())
        overlaps: dict[str, list[int]] = {}
        for key in reserved:
            match = re.fullmatch(r"(\d{4})-(\d{4})", str(key))
            if not match:
                continue
            low, high = int(match.group(1)), int(match.group(2))
            hits = sorted(p for p in allocated if low <= p <= high)
            if hits:
                overlaps[str(key)] = hits
        assert overlaps == {}, f"reserved ranges overlap allocations: {overlaps}"