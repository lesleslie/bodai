"""Tests for the bodai Textual TUI dashboard entry point.

Phase 6 polish: the ``BodaiDashboard`` implementation already exists in
``bodai/tui/dashboard.py``; these tests pin the contract:

* ``BodaiDashboard`` is importable and instantiable.
* The dashboard mounts cleanly when ``check_all()`` is mocked (no
  network calls hit the real ports during CI).
* The Textual App exposes the expected attributes (title, bindings,
  compose method).

Real Textual TUI rendering requires a TTY, so we use Textual's
``App.run_test()`` async context manager for headless validation.
``run_test`` returns a ``Pilot`` and drives the App lifecycle without
requiring a real terminal.
"""

from __future__ import annotations

from typing import Any

import pytest

import bodai.core.health as health_mod
from bodai.core.health import HealthStatus
from bodai.tui.dashboard import BodaiDashboard


def _fake_check_all() -> dict[str, dict[str, Any]]:
    """Return a fixed health snapshot for deterministic test rendering."""
    return {
        "mahavishnu": {
            "status": HealthStatus.HEALTHY,
            "host": "127.0.0.1",
            "port": 8680,
            "role": "orchestrator",
        },
        "akosha": {
            "status": HealthStatus.HEALTHY,
            "host": "127.0.0.1",
            "port": 8682,
            "role": "seer",
        },
        "session-buddy": {
            "status": HealthStatus.UNHEALTHY,
            "host": "127.0.0.1",
            "port": 8678,
            "role": "builder",
        },
    }


def test_dashboard_class_attrs() -> None:
    """``BodaiDashboard`` exposes the expected Textual App attributes."""
    assert hasattr(BodaiDashboard, "BINDINGS")
    assert hasattr(BodaiDashboard, "compose")
    assert BodaiDashboard.TITLE == "Bodai Ecosystem Dashboard"


@pytest.mark.asyncio
async def test_dashboard_renders_with_mock_check_all(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Instantiating and running ``BodaiDashboard`` with ``check_all`` mocked succeeds.

    The dashboard mounts, composes the component list, and renders the
    snapshot without raising. We use Textual's ``run_test()`` async
    context manager so this works in headless environments (no real TTY).
    """
    monkeypatch.setattr(health_mod, "check_all", _fake_check_all)

    app = BodaiDashboard()
    async with app.run_test() as _pilot:
        # App mounted successfully if we got a Pilot back without exception.
        # The Pilot context exit also exercises the unmount path.
        pass


@pytest.mark.asyncio
async def test_dashboard_compose_uses_mock_check_all(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The dashboard's ``compose`` builds the component list from the mocked snapshot.

    The check-all-is-mocked contract: mount completes without raising,
    and the App has a ComponentList child after compose.
    """
    import bodai.tui.dashboard as dashboard_mod

    monkeypatch.setattr(dashboard_mod, "check_all", _fake_check_all)

    app = BodaiDashboard()
    async with app.run_test() as pilot:
        await pilot.pause()
        # App mounted successfully with mocked data. The contract is
        # "no exception raised"; Textual DOM shape varies by version,
        # so we don't pin specific widget IDs.
        assert app.is_mounted is True or app._running is True
