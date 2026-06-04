"""Integration tests for iec check with real checkers."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from iec_cli.check import registry
from iec_cli.checkers.adr_format import AdrFormat
from iec_cli.checkers.adr_index import AdrIndex
from iec_cli.checkers.agents_exists import AgentsExists
from iec_cli.checkers.agents_hub_structure import AgentsHubStructure
from iec_cli.checkers.agents_links import AgentsLinks
from iec_cli.checkers.agents_size import AgentsSize
from iec_cli.checkers.docs_index_exists import DocsIndexExists
from iec_cli.checkers.docs_index_stale import DocsIndexStale
from iec_cli.checkers.docs_readme_exists import DocsReadmeExists
from iec_cli.checkers.file_size import FileSize
from iec_cli.checkers.secrets import Secrets
from iec_cli.checkers.spec_ac_ids import SpecAcIds
from iec_cli.checkers.spec_size import SpecSize
from iec_cli.checkers.spec_test_category import SpecTestCategory
from iec_cli.checkers.test_coverage import TestCoverage
from iec_cli.checkers.test_traceability import TestTraceability
from iec_cli.main import app

runner = CliRunner()


def _register_all() -> None:
    registry.register(AgentsExists)
    registry.register(AgentsSize)
    registry.register(AgentsLinks)
    registry.register(DocsReadmeExists)
    registry.register(DocsIndexExists)
    registry.register(DocsIndexStale)
    registry.register(AdrFormat)
    registry.register(AdrIndex)
    registry.register(SpecAcIds)
    registry.register(SpecTestCategory)
    registry.register(SpecSize)
    registry.register(FileSize)
    registry.register(AgentsHubStructure)
    registry.register(Secrets)
    registry.register(TestTraceability)
    registry.register(TestCoverage)


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    """Reset registry and re-register checkers before each test."""
    registry._checkers.clear()
    _register_all()


def test_ase_check_runs_all_checkers() -> None:
    """Covers: AGEX-001, AGSZ-001, AGLN-001, ADRF-001, ADRI-001
    ACID-002, STCT-002, AHUB-001, SECR-001"""
    result = runner.invoke(app, ["check"])
    assert "agents-exists" in result.stdout
    assert "agents-size" in result.stdout
    assert "agents-links" in result.stdout
    assert "docs-readme-exists" in result.stdout
    assert "docs-index-exists" in result.stdout
    assert "docs-index-stale" in result.stdout
    assert "adr-format" in result.stdout
    assert "adr-index" in result.stdout
    assert "spec-ac-ids" in result.stdout
    assert "spec-test-category" in result.stdout
    assert "spec-size" in result.stdout
    assert "file-size" in result.stdout
    assert "agents-hub-structure" in result.stdout
    assert "secrets" in result.stdout
    assert "test-traceability" in result.stdout
    assert "test-coverage" in result.stdout
    assert "check(s)" in result.stdout


def test_ase_check_missing_agents_md(tmp_path: Path) -> None:
    """Covers: AGEX-002, AGSZ-004, AGLN-005"""
    result = runner.invoke(app, ["check", "--path", str(tmp_path)])
    assert result.exit_code == 2  # failures
    assert "agents-exists" in result.stdout
    assert "FAIL" in result.stdout
    assert "not found" in result.stdout.lower()
