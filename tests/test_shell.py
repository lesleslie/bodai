"""Tests for the bodai.admin.shell entry point.

Phase 6 verifies that the IPython admin shell is wired through
``bodai.cli`` without defensive ``try/except ImportError`` gates. These
tests assert the import path resolves and the CLI subcommand exposes
its Typer surface via ``--help``.
"""

from typer.testing import CliRunner

from bodai.admin.shell import launch_shell
from bodai.cli import app

runner = CliRunner()


def test_launch_shell_callable() -> None:
    """``bodai.admin.shell.launch_shell`` is importable and callable."""
    assert callable(launch_shell)


def test_bodai_shell_help_exits_zero() -> None:
    """``bodai shell --help`` exits 0 (no defensive ImportError fallback)."""
    result = runner.invoke(app, ["shell", "--help"])
    assert result.exit_code == 0
