"""Tests for the bodai IPython admin shell entry point.

Phase 6 polish: the ``launch_shell()`` implementation already exists in
``bodai/admin/shell.py``; these tests pin the contract:

* ``launch_shell()`` populates an IPython namespace with the canonical
  ecosystem objects (config loaders, health probes, models, components).
* When the underlying ``IPython`` import fails the friendly installer
  hint bubbles out (the CLI subcommand catches it and exits 1; we
  assert the same path through the module function itself).

The real IPython REPL is interactive, so we mock ``IPython.start_ipython``
to record the namespace without actually entering a REPL.
"""

from __future__ import annotations

from typing import Any

import pytest
from typer.testing import CliRunner

import bodai.admin.shell as bodai_shell
import bodai.cli as bodai_cli
import bodai.tui.dashboard as dashboard_mod

runner = CliRunner()


@pytest.fixture
def fake_ipython(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Patch ``IPython.start_ipython`` to capture the ``user_ns``.

    Returns a dict with the recorded ``user_ns`` payload so individual
    tests can introspect what the shell pre-loaded.
    """
    recorded: dict[str, Any] = {}

    def fake_start_ipython(*, argv: list[str], user_ns: dict[str, Any]) -> None:
        recorded["argv"] = list(argv)
        recorded["user_ns"] = dict(user_ns)

    import IPython  # type: ignore[import-not-found]

    monkeypatch.setattr(IPython, "start_ipython", fake_start_ipython)
    return recorded


def test_launch_shell_invokes_ipython_with_namespace(
    fake_ipython: dict[str, Any],
) -> None:
    """``launch_shell`` calls ``IPython.start_ipython`` with the canonical namespace.

    The pre-loaded namespace must include the config objects, health
    functions, and every registered ecosystem component name. This pins
    the contract documented in ``docs/plans/2026-08-25-bodai-tui-shell-surface.md``.
    """
    bodai_shell.launch_shell()

    assert "user_ns" in fake_ipython, "IPython.start_ipython was never called"
    user_ns = fake_ipython["user_ns"]

    # Config objects (per shell.py::launch_shell)
    for key in ("ecosystem", "portmap", "storage_map"):
        assert key in user_ns, f"namespace missing {key!r}"

    # Config loader functions
    for key in ("load_ecosystem", "load_portmap", "load_storage_map"):
        assert key in user_ns, f"namespace missing loader {key!r}"

    # Health probes
    assert "check_all" in user_ns
    assert "check_component" in user_ns

    # Models
    assert "Component" in user_ns
    assert "Ecosystem" in user_ns

    # Per-component variables (one per registered component)
    ecosystem_obj = user_ns["ecosystem"]
    for comp_name in ecosystem_obj.components:
        assert comp_name in user_ns, f"component {comp_name!r} not exposed"


def test_shell_cli_subcommand_import_error_exits_with_installer_hint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When ``from bodai.admin.shell import launch_shell`` fails with ImportError,
    the CLI subcommand prints the installer hint and exits 1 (not silently swallowed).
    """
    # Delete the ``launch_shell`` attribute from ``bodai.admin.shell`` so the
    # CLI's ``from bodai.admin.shell import launch_shell`` raises ImportError
    # on attribute lookup. monkeypatch restores the attribute on teardown.
    monkeypatch.delattr(bodai_shell, "launch_shell", raising=True)

    result = runner.invoke(bodai_cli.app, ["shell"])

    # Friendly error path: non-zero exit, hint in output.
    assert result.exit_code != 0, (
        f"expected non-zero exit; got {result.exit_code}\n{result.output!r}"
    )
    combined = result.output or ""
    assert "uv pip install" in combined, (
        f"installer hint missing from output: {combined!r}"
    )
    assert "shell extra" in combined, (
        f"shell extra hint missing from output: {combined!r}"
    )


def test_dashboard_cli_subcommand_import_error_exits_with_installer_hint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Symmetric test for the dashboard subcommand's friendly ImportError handling.

    Guards against the defensive ``try/except ImportError: print 'not yet implemented'``
    pattern that was previously in bodai/cli.py.
    """
    monkeypatch.delattr(dashboard_mod, "BodaiDashboard", raising=True)

    result = runner.invoke(bodai_cli.app, ["dashboard"])

    assert result.exit_code != 0
    combined = result.output or ""
    assert "uv pip install" in combined
    assert "shell extra" in combined
