"""Integration tests for ase check with real checkers."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from ase_cli.check import registry
from ase_cli.checkers.agents_exists import AgentsExists
from ase_cli.checkers.agents_links import AgentsLinks
from ase_cli.checkers.agents_size import AgentsSize
from ase_cli.main import app

runner = CliRunner()


def _register_all() -> None:
    registry.register(AgentsExists)
    registry.register(AgentsSize)
    registry.register(AgentsLinks)


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    """Reset registry and re-register checkers before each test."""
    registry._checkers.clear()
    _register_all()


def test_ase_check_runs_all_checkers() -> None:
    """Covers: AGEX-001, AGSZ-001, AGLN-001 — real checkers against ase-cli repo"""
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0
    assert "agents-exists" in result.stdout
    assert "agents-size" in result.stdout
    assert "agents-links" in result.stdout
    assert "passed" in result.stdout


def test_ase_check_missing_agents_md(tmp_path: Path) -> None:
    """Covers: AGEX-002, AGSZ-004, AGLN-005"""
    result = runner.invoke(app, ["check", "--path", str(tmp_path)])
    assert result.exit_code == 2  # failures
    assert "agents-exists" in result.stdout
    assert "FAIL" in result.stdout
    assert "not found" in result.stdout.lower()
