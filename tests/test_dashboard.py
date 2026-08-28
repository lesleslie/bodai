"""Tests for the bodai.tui.dashboard entry point.

Phase 6 verifies that the Textual TUI dashboard is wired through
``bodai.cli`` without defensive ``try/except ImportError`` gates. These
tests assert the import path resolves and the CLI subcommand exposes
its Typer surface via ``--help``.
"""

from typer.testing import CliRunner

from bodai.cli import app
from bodai.tui.dashboard import BodaiDashboard

runner = CliRunner()


def test_bodai_dashboard_callable() -> None:
    """``bodai.tui.dashboard.BodaiDashboard`` is importable and callable."""
    assert callable(BodaiDashboard)


def test_bodai_dashboard_help_exits_zero() -> None:
    """``bodai dashboard --help`` exits 0 (no defensive ImportError fallback)."""
    result = runner.invoke(app, ["dashboard", "--help"])
    assert result.exit_code == 0


def test_bodai_dashboard_class_attrs() -> None:
    """``BodaiDashboard`` exposes the expected Textual App attributes."""
    assert hasattr(BodaiDashboard, "CSS_PATH")
    assert hasattr(BodaiDashboard, "BINDINGS")
    assert isinstance(BodaiDashboard.BINDINGS, list)
    assert len(BodaiDashboard.BINDINGS) >= 1
