"""Unit tests for ADR format and index checkers."""

import shutil
from pathlib import Path

from iec_cli.check import Registry, Status
from iec_cli.checkers import adr_format, adr_index

FIXTURES = Path(__file__).parent / "fixtures" / "adr"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _place(base: Path, fixture: str, filename: str) -> Path:
    """Copy fixture into docs/decisions/<filename>."""
    decisions = base / "docs" / "decisions"
    decisions.mkdir(parents=True, exist_ok=True)
    dest = decisions / filename
    shutil.copy(FIXTURES / fixture, dest)
    return dest


def _write_readme(base: Path, content: str) -> Path:
    readme = base / "docs" / "decisions" / "README.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    readme.write_text(content)
    return readme


# ---------------------------------------------------------------------------
# adr-format
# ---------------------------------------------------------------------------


def test_format_valid_bullet(tmp_path: Path) -> None:
    """Covers: ADRF-001, ADRF-007"""
    _place(tmp_path, "valid_bullet.md", "0001-example.md")
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.PASS


def test_format_invalid_filename(tmp_path: Path) -> None:
    """Covers: ADRF-002"""
    _place(tmp_path, "valid_bullet.md", "my-decision.md")
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.FAIL
    assert "my-decision.md" in result.message


def test_format_missing_title_heading(tmp_path: Path) -> None:
    """Covers: ADRF-003"""
    _place(tmp_path, "missing_title.md", "0001-example.md")
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.FAIL
    assert "title heading" in result.message


def test_format_title_number_mismatch(tmp_path: Path) -> None:
    """Covers: ADRF-004"""
    _place(tmp_path, "title_mismatch.md", "0001-example.md")
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.FAIL
    assert "0001" in result.message
    assert "0002" in result.message


def test_format_missing_context_section(tmp_path: Path) -> None:
    """Covers: ADRF-005"""
    _place(tmp_path, "missing_context.md", "0001-example.md")
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.FAIL
    assert "Context and Problem Statement" in result.message


def test_format_missing_decision_outcome(tmp_path: Path) -> None:
    """Covers: ADRF-006"""
    _place(tmp_path, "missing_decision.md", "0001-example.md")
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.FAIL
    assert "Decision Outcome" in result.message


def test_format_missing_status(tmp_path: Path) -> None:
    """Covers: ADRF-008"""
    _place(tmp_path, "missing_status.md", "0001-example.md")
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.FAIL
    assert "missing status" in result.message


def test_format_invalid_status_bullet(tmp_path: Path) -> None:
    """Covers: ADRF-009"""
    _place(tmp_path, "invalid_status_bullet.md", "0001-example.md")
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.FAIL
    assert "draft" in result.message


def test_format_no_decisions_dir(tmp_path: Path) -> None:
    """Covers: ADRF-010 — missing docs/decisions/"""
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.PASS


def test_format_empty_decisions_dir(tmp_path: Path) -> None:
    """Covers: ADRF-010 — empty docs/decisions/"""
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.PASS


def test_format_registered() -> None:
    """Covers: ADRF-011"""
    reg = Registry()
    reg.register(adr_format.AdrFormat)
    assert "adr-format" in [c[0] for c in reg.list_all()]


def test_format_valid_yaml_plain_title(tmp_path: Path) -> None:
    """Covers: ADRF-012, ADRF-013 — YAML front matter with plain title"""
    _place(tmp_path, "valid_yaml.md", "0001-example.md")
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.PASS


def test_format_invalid_status_yaml(tmp_path: Path) -> None:
    """Covers: ADRF-014"""
    _place(tmp_path, "invalid_status_yaml.md", "0001-example.md")
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.FAIL
    assert "draft" in result.message


def test_format_superseded_with_reference(tmp_path: Path) -> None:
    """Covers: ADRF-015 — 'superseded by [ADR-XXXX]' starts with valid prefix"""
    _place(tmp_path, "superseded_bullet.md", "0001-example.md")
    result = adr_format.AdrFormat().check(tmp_path)
    assert result.status == Status.PASS


# ---------------------------------------------------------------------------
# adr-index
# ---------------------------------------------------------------------------


def test_index_all_listed(tmp_path: Path) -> None:
    """Covers: ADRI-001, ADRI-004"""
    _place(tmp_path, "valid_bullet.md", "0001-example.md")
    _write_readme(tmp_path, "| [0001](0001-example.md) | Example |\n")
    result = adr_index.AdrIndex().check(tmp_path)
    assert result.status == Status.PASS


def test_index_readme_missing_with_adrs(tmp_path: Path) -> None:
    """Covers: ADRI-002"""
    _place(tmp_path, "valid_bullet.md", "0001-example.md")
    result = adr_index.AdrIndex().check(tmp_path)
    assert result.status == Status.FAIL
    assert "README.md missing" in result.message


def test_index_no_decisions_dir(tmp_path: Path) -> None:
    """Covers: ADRI-003 — missing docs/decisions/"""
    result = adr_index.AdrIndex().check(tmp_path)
    assert result.status == Status.PASS


def test_index_empty_decisions_dir(tmp_path: Path) -> None:
    """Covers: ADRI-003 — empty docs/decisions/"""
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    result = adr_index.AdrIndex().check(tmp_path)
    assert result.status == Status.PASS


def test_index_one_adr_unlisted(tmp_path: Path) -> None:
    """Covers: ADRI-005"""
    _place(tmp_path, "valid_bullet.md", "0001-example.md")
    _place(tmp_path, "valid_bullet.md", "0002-another.md")
    _write_readme(tmp_path, "| [0001](0001-example.md) | Example |\n")
    result = adr_index.AdrIndex().check(tmp_path)
    assert result.status == Status.FAIL
    assert "0002-another.md" in result.message


def test_index_multiple_adrs_unlisted(tmp_path: Path) -> None:
    """Covers: ADRI-006"""
    _place(tmp_path, "valid_bullet.md", "0001-example.md")
    _place(tmp_path, "valid_bullet.md", "0002-another.md")
    _place(tmp_path, "valid_bullet.md", "0003-third.md")
    _write_readme(tmp_path, "| [0001](0001-example.md) | Example |\n")
    result = adr_index.AdrIndex().check(tmp_path)
    assert result.status == Status.FAIL
    assert "0002-another.md" in result.message
    assert "0003-third.md" in result.message


def test_index_registered() -> None:
    """Covers: ADRI-007"""
    reg = Registry()
    reg.register(adr_index.AdrIndex)
    assert "adr-index" in [c[0] for c in reg.list_all()]
