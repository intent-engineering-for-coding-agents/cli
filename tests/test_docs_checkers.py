"""Unit tests for architecture & file structure checkers."""

from pathlib import Path

from ase_cli.check import Registry, Status
from ase_cli.checkers import (
    docs_index_exists,
    docs_index_stale,
    docs_readme_exists,
)


def _make_tree(base: Path, *paths: str) -> None:
    """Create files/dirs from a list of relative paths under base."""
    for p in paths:
        target = base / p
        target.parent.mkdir(parents=True, exist_ok=True)
        target.touch()


# ---------------------------------------------------------------------------
# docs-readme-exists
# ---------------------------------------------------------------------------


def test_readme_all_present(tmp_path: Path) -> None:
    """Covers: DRME-001"""
    _make_tree(tmp_path, "docs/README.md", "docs/architecture/README.md")
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.PASS


def test_readme_one_missing(tmp_path: Path) -> None:
    """Covers: DRME-002"""
    _make_tree(tmp_path, "docs/README.md")
    (tmp_path / "docs" / "architecture").mkdir(parents=True)
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.FAIL
    assert "docs/architecture" in result.message


def test_readme_multiple_missing(tmp_path: Path) -> None:
    """Covers: DRME-003"""
    _make_tree(tmp_path, "docs/README.md")
    (tmp_path / "docs" / "architecture").mkdir(parents=True)
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.FAIL
    assert "architecture" in result.message
    assert "decisions" in result.message


def test_readme_docs_missing(tmp_path: Path) -> None:
    """Covers: DRME-004"""
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.FAIL
    assert "not found" in result.message.lower()


def test_readme_registered() -> None:
    """Covers: DRME-005"""
    reg = Registry()
    reg.register(docs_readme_exists.DocsReadmeExists)
    assert "docs-readme-exists" in [c[0] for c in reg.list_all()]


# ---------------------------------------------------------------------------
# docs-index-exists
# ---------------------------------------------------------------------------


def test_index_all_present(tmp_path: Path) -> None:
    """Covers: DINE-001"""
    _make_tree(tmp_path, "docs/INDEX.md", "docs/architecture/INDEX.md")
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.PASS


def test_index_one_missing(tmp_path: Path) -> None:
    """Covers: DINE-002"""
    _make_tree(tmp_path, "docs/INDEX.md")
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.WARN
    assert "docs/decisions" in result.message


def test_index_multiple_missing(tmp_path: Path) -> None:
    """Covers: DINE-003"""
    _make_tree(tmp_path, "docs/INDEX.md")
    (tmp_path / "docs" / "architecture").mkdir(parents=True)
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.WARN
    assert "architecture" in result.message
    assert "decisions" in result.message


def test_index_docs_missing(tmp_path: Path) -> None:
    """Covers: DINE-004"""
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.FAIL
    assert "not found" in result.message.lower()


def test_index_registered() -> None:
    """Covers: DINE-005"""
    reg = Registry()
    reg.register(docs_index_exists.DocsIndexExists)
    assert "docs-index-exists" in [c[0] for c in reg.list_all()]


# ---------------------------------------------------------------------------
# docs-index-stale
# ---------------------------------------------------------------------------


def test_stale_all_match(tmp_path: Path) -> None:
    """Covers: DINS-001"""
    _make_tree(tmp_path, "docs/a.md", "docs/b.md")
    (tmp_path / "docs" / "INDEX.md").write_text("- [A](a.md)\n- [B](b.md)\n")
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.PASS


def test_stale_broken_link(tmp_path: Path) -> None:
    """Covers: DINS-002"""
    _make_tree(tmp_path, "docs/a.md")
    (tmp_path / "docs" / "INDEX.md").write_text(
        "- [A](a.md)\n- [Missing](missing.md)\n"
    )
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.WARN
    assert "Broken" in result.message
    assert "missing.md" in result.message


def test_stale_orphan_file(tmp_path: Path) -> None:
    """Covers: DINS-003"""
    _make_tree(tmp_path, "docs/a.md", "docs/unlisted.md")
    (tmp_path / "docs" / "INDEX.md").write_text("- [A](a.md)\n")
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.WARN
    assert "Orphan" in result.message
    assert "unlisted.md" in result.message


def test_stale_broken_and_orphan(tmp_path: Path) -> None:
    """Covers: DINS-004"""
    _make_tree(tmp_path, "docs/index.md", "docs/unlisted.md")
    (tmp_path / "docs" / "INDEX.md").write_text(
        "- [Index](index.md)\n- [Missing](gone.md)\n"
    )
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.WARN
    assert "Broken" in result.message
    assert "Orphan" in result.message


def test_stale_gitkeep_excluded(tmp_path: Path) -> None:
    """Covers: DINS-005"""
    _make_tree(tmp_path, "docs/a.md", "docs/.gitkeep")
    (tmp_path / "docs" / "INDEX.md").write_text("- [A](a.md)\n")
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.PASS


def test_stale_docs_missing(tmp_path: Path) -> None:
    """Covers: DINS-006"""
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.FAIL
    assert "not found" in result.message.lower()


def test_stale_registered() -> None:
    """Covers: DINS-007"""
    reg = Registry()
    reg.register(docs_index_stale.DocsIndexStale)
    assert "docs-index-stale" in [c[0] for c in reg.list_all()]
