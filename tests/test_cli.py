"""Tests for CLI commands."""

from typer.testing import CliRunner

from bodai.cli import app

runner = CliRunner()


def test_cli_help():
    """Test CLI help output."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "bodai" in result.output.lower()


def test_health_command():
    """Test health check command."""
    result = runner.invoke(app, ["health"])
    assert result.exit_code == 0


def test_config_show_command():
    """Test config show command."""
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
