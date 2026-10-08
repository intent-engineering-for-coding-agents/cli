"""Unit tests for architecture & file structure checkers."""

from pathlib import Path

import pytest

from iec_cli.check import Registry, Status
from iec_cli.checkers import (
    docs_index_exists,
    docs_index_scope,
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


@pytest.mark.unit
@pytest.mark.ac("DRME-001")
def test_readme_all_present(tmp_path: Path) -> None:
    """Covers: DRME-001"""
    _make_tree(tmp_path, "docs/README.md", "docs/architecture/README.md")
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DRME-002")
def test_readme_one_missing(tmp_path: Path) -> None:
    """Covers: DRME-002"""
    _make_tree(tmp_path, "docs/README.md", "docs/architecture/overview.md")
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.FAIL
    assert "docs/architecture" in result.message


@pytest.mark.unit
@pytest.mark.ac("DRME-003")
def test_readme_multiple_missing(tmp_path: Path) -> None:
    """Covers: DRME-003"""
    _make_tree(
        tmp_path,
        "docs/README.md",
        "docs/architecture/overview.md",
        "docs/decisions/0001-x.md",
    )
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.FAIL
    assert "architecture" in result.message
    assert "decisions" in result.message


@pytest.mark.unit
@pytest.mark.ac("DRME-004")
def test_readme_docs_missing(tmp_path: Path) -> None:
    """Covers: DRME-004"""
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.FAIL
    assert "not found" in result.message.lower()


@pytest.mark.unit
@pytest.mark.ac("DRME-005")
def test_readme_registered() -> None:
    """Covers: DRME-005"""
    reg = Registry()
    reg.register(docs_readme_exists.DocsReadmeExists)
    assert "docs-readme-exists" in [c[0] for c in reg.list_all()]


@pytest.mark.unit
@pytest.mark.ac("DRME-006")
def test_readme_gitkeep_only_subdir_exempt(tmp_path: Path) -> None:
    """Covers: DRME-006 — directory containing only .gitkeep is skipped."""
    _make_tree(tmp_path, "docs/README.md", "docs/design/.gitkeep")
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.PASS
    assert "docs/design" not in result.message


@pytest.mark.unit
@pytest.mark.ac("DRME-006")
def test_readme_dotfiles_only_subdir_exempt(tmp_path: Path) -> None:
    """Covers: DRME-006 — directory containing only dotfiles is skipped."""
    _make_tree(
        tmp_path,
        "docs/README.md",
        "docs/design/.gitkeep",
        "docs/design/.hidden",
        "docs/design/.DS_Store",
    )
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DRME-006")
def test_readme_nested_empty_subdir_exempt(tmp_path: Path) -> None:
    """Covers: DRME-006 — nested subdirectory with only a placeholder is skipped."""
    _make_tree(tmp_path, "docs/README.md", "docs/design/wip/.gitkeep")
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DRME-006")
def test_readme_gitkeep_plus_real_file_still_fails(tmp_path: Path) -> None:
    """Covers: DRME-006 — a real file alongside .gitkeep is substantive content."""
    _make_tree(
        tmp_path,
        "docs/README.md",
        "docs/design/.gitkeep",
        "docs/design/draft.md",
    )
    result = docs_readme_exists.DocsReadmeExists().check(tmp_path)
    assert result.status == Status.FAIL
    assert "docs/design" in result.message


# ---------------------------------------------------------------------------
# docs-index-exists
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.ac("DINE-001")
def test_index_all_present(tmp_path: Path) -> None:
    """Covers: DINE-001"""
    _make_tree(tmp_path, "docs/INDEX.md", "docs/architecture/INDEX.md")
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DINE-002")
def test_index_one_missing(tmp_path: Path) -> None:
    """Covers: DINE-002"""
    _make_tree(tmp_path, "docs/INDEX.md", "docs/decisions/0001-x.md")
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.WARN
    assert "docs/decisions" in result.message


@pytest.mark.unit
@pytest.mark.ac("DINE-003")
def test_index_multiple_missing(tmp_path: Path) -> None:
    """Covers: DINE-003"""
    _make_tree(
        tmp_path,
        "docs/INDEX.md",
        "docs/architecture/overview.md",
        "docs/decisions/0001-x.md",
    )
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.WARN
    assert "architecture" in result.message
    assert "decisions" in result.message


@pytest.mark.unit
@pytest.mark.ac("DINE-004")
def test_index_docs_missing(tmp_path: Path) -> None:
    """Covers: DINE-004"""
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.FAIL
    assert "not found" in result.message.lower()


@pytest.mark.unit
@pytest.mark.ac("DINE-005")
def test_index_registered() -> None:
    """Covers: DINE-005"""
    reg = Registry()
    reg.register(docs_index_exists.DocsIndexExists)
    assert "docs-index-exists" in [c[0] for c in reg.list_all()]


@pytest.mark.unit
@pytest.mark.ac("DINE-006")
def test_index_gitkeep_only_subdir_exempt(tmp_path: Path) -> None:
    """Covers: DINE-006 — directory containing only .gitkeep is skipped."""
    _make_tree(tmp_path, "docs/INDEX.md", "docs/design/.gitkeep")
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.PASS
    assert "docs/design" not in result.message


@pytest.mark.unit
@pytest.mark.ac("DINE-006")
def test_index_dotfiles_only_subdir_exempt(tmp_path: Path) -> None:
    """Covers: DINE-006 — directory containing only dotfiles is skipped."""
    _make_tree(
        tmp_path,
        "docs/INDEX.md",
        "docs/design/.gitkeep",
        "docs/design/.hidden",
        "docs/design/.DS_Store",
    )
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DINE-006")
def test_index_nested_empty_subdir_exempt(tmp_path: Path) -> None:
    """Covers: DINE-006 — nested subdirectory with only a placeholder is skipped."""
    _make_tree(tmp_path, "docs/INDEX.md", "docs/design/wip/.gitkeep")
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DINE-006")
def test_index_gitkeep_plus_real_file_still_warns(tmp_path: Path) -> None:
    """Covers: DINE-006 — a real file alongside .gitkeep is substantive content."""
    _make_tree(
        tmp_path,
        "docs/INDEX.md",
        "docs/design/.gitkeep",
        "docs/design/draft.md",
    )
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.WARN
    assert "docs/design" in result.message


# ---------------------------------------------------------------------------
# docs-index-stale
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.ac("DINS-001")
def test_stale_all_match(tmp_path: Path) -> None:
    """Covers: DINS-001"""
    _make_tree(tmp_path, "docs/a.md", "docs/b.md")
    (tmp_path / "docs" / "INDEX.md").write_text("- [A](a.md)\n- [B](b.md)\n")
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DINS-002")
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


@pytest.mark.unit
@pytest.mark.ac("DINS-003")
def test_stale_orphan_file(tmp_path: Path) -> None:
    """Covers: DINS-003"""
    _make_tree(tmp_path, "docs/a.md", "docs/unlisted.md")
    (tmp_path / "docs" / "INDEX.md").write_text("- [A](a.md)\n")
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.WARN
    assert "Orphan" in result.message
    assert "unlisted.md" in result.message


@pytest.mark.unit
@pytest.mark.ac("DINS-004")
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


@pytest.mark.unit
@pytest.mark.ac("DINS-005")
def test_stale_gitkeep_excluded(tmp_path: Path) -> None:
    """Covers: DINS-005"""
    _make_tree(tmp_path, "docs/a.md", "docs/.gitkeep")
    (tmp_path / "docs" / "INDEX.md").write_text("- [A](a.md)\n")
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DINS-006")
def test_stale_docs_missing(tmp_path: Path) -> None:
    """Covers: DINS-006"""
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.FAIL
    assert "not found" in result.message.lower()


@pytest.mark.unit
@pytest.mark.ac("DINS-007")
def test_stale_registered() -> None:
    """Covers: DINS-007"""
    reg = Registry()
    reg.register(docs_index_stale.DocsIndexStale)
    assert "docs-index-stale" in [c[0] for c in reg.list_all()]


# ---------------------------------------------------------------------------
# docs-index-scope
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.ac("DISO-001")
def test_scope_same_dir_file_link(tmp_path: Path) -> None:
    """Covers: DISO-001 — same-directory file link is in scope."""
    _make_tree(tmp_path, "docs/a.md")
    (tmp_path / "docs" / "INDEX.md").write_text("- [A](a.md)\n")
    result = docs_index_scope.DocsIndexScope().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DISO-002")
def test_scope_subdir_index_pointer(tmp_path: Path) -> None:
    """Covers: DISO-002 — immediate subdir/INDEX.md pointer is in scope."""
    _make_tree(tmp_path, "docs/decisions/INDEX.md")
    (tmp_path / "docs" / "INDEX.md").write_text("- [Decisions](decisions/INDEX.md)\n")
    result = docs_index_scope.DocsIndexScope().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DISO-003")
def test_scope_subdir_readme_pointer(tmp_path: Path) -> None:
    """Covers: DISO-003 — immediate subdir/README.md pointer is in scope."""
    _make_tree(tmp_path, "docs/decisions/README.md")
    (tmp_path / "docs" / "INDEX.md").write_text("- [Decisions](decisions/README.md)\n")
    result = docs_index_scope.DocsIndexScope().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DISO-004")
def test_scope_deeper_path_flagged(tmp_path: Path) -> None:
    """Covers: DISO-004 — deeper paths reach into a sub-INDEX's territory."""
    _make_tree(tmp_path, "docs/decisions/0001-x.md")
    (tmp_path / "docs" / "INDEX.md").write_text("- [ADR-0001](decisions/0001-x.md)\n")
    result = docs_index_scope.DocsIndexScope().check(tmp_path)
    assert result.status == Status.WARN
    assert "decisions/0001-x.md" in result.message


@pytest.mark.unit
@pytest.mark.ac("DISO-005")
def test_scope_parent_path_flagged(tmp_path: Path) -> None:
    """Covers: DISO-005 — parent paths point outside the docs tree."""
    _make_tree(tmp_path, "docs/AGENTS.md")
    (tmp_path / "docs" / "INDEX.md").write_text("- [Agents](../AGENTS.md)\n")
    result = docs_index_scope.DocsIndexScope().check(tmp_path)
    assert result.status == Status.WARN
    assert "../AGENTS.md" in result.message


@pytest.mark.unit
@pytest.mark.ac("DISO-006")
def test_scope_absolute_url_flagged(tmp_path: Path) -> None:
    """Covers: DISO-006 — absolute URLs belong in README prose, not INDEX."""
    _make_tree(tmp_path, "docs/a.md")
    (tmp_path / "docs" / "INDEX.md").write_text("- [External](https://example.com/x)\n")
    result = docs_index_scope.DocsIndexScope().check(tmp_path)
    assert result.status == Status.WARN
    assert "https://example.com/x" in result.message


@pytest.mark.unit
@pytest.mark.ac("DISO-007")
def test_scope_skips_dirs_without_index(tmp_path: Path) -> None:
    """Covers: DISO-007 — checker is not redundant with docs-index-exists."""
    _make_tree(tmp_path, "docs/decisions/0001-x.md")
    # No INDEX.md anywhere — scope checker has nothing to inspect, returns PASS
    result = docs_index_scope.DocsIndexScope().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DISO-008")
def test_scope_registered() -> None:
    """Covers: DISO-008"""
    reg = Registry()
    reg.register(docs_index_scope.DocsIndexScope)
    assert "docs-index-scope" in [c[0] for c in reg.list_all()]


@pytest.mark.unit
@pytest.mark.baseline
def test_scope_docs_missing(tmp_path: Path) -> None:
    """docs/ missing returns FAIL (consistent with sibling checkers)."""
    result = docs_index_scope.DocsIndexScope().check(tmp_path)
    assert result.status == Status.FAIL
    assert "not found" in result.message.lower()


# ---------------------------------------------------------------------------
# embedded README index (docs-index-exists, docs-index-stale, docs-index-scope)
# ---------------------------------------------------------------------------


def _readme_with_block(base: Path, rel_dir: str, *rows: str, prose: str = "") -> None:
    """Write a README.md holding an index block with the given rows."""
    target = base / rel_dir / "README.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(rows)
    target.write_text(
        f"# Title\n\n{prose}\n<!-- index:start -->\n{body}\n<!-- index:end -->\n"
    )


@pytest.mark.unit
@pytest.mark.ac("DINE-007")
def test_index_exists_embedded_block_counts(tmp_path: Path) -> None:
    """Covers: DINE-007"""
    _make_tree(tmp_path, "docs/a.md")
    _readme_with_block(tmp_path, "docs", "| [A](a.md) | The A file |")
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DINE-008")
def test_index_exists_readme_without_block_warns(tmp_path: Path) -> None:
    """Covers: DINE-008"""
    _make_tree(tmp_path, "docs/a.md")
    (tmp_path / "docs" / "README.md").write_text("# Docs\n\nNo index here.\n")
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.WARN
    assert "docs" in result.message


@pytest.mark.unit
@pytest.mark.ac("DINE-009")
def test_index_exists_unterminated_block_warns(tmp_path: Path) -> None:
    """Covers: DINE-009"""
    _make_tree(tmp_path, "docs/a.md")
    (tmp_path / "docs" / "README.md").write_text(
        "# Docs\n\n<!-- index:start -->\n| [A](a.md) | A |\n"
    )
    result = docs_index_exists.DocsIndexExists().check(tmp_path)
    assert result.status == Status.WARN


@pytest.mark.unit
@pytest.mark.ac("DINS-008")
def test_stale_embedded_block_matches(tmp_path: Path) -> None:
    """Covers: DINS-008 -- README.md hosts the block and is not an orphan."""
    _make_tree(tmp_path, "docs/a.md")
    _readme_with_block(
        tmp_path,
        "docs",
        "| [A](a.md) | The A file |",
        prose="See [elsewhere](missing.md) for background.\n",
    )
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DINS-009")
def test_stale_embedded_block_orphan(tmp_path: Path) -> None:
    """Covers: DINS-009"""
    _make_tree(tmp_path, "docs/a.md", "docs/b.md")
    _readme_with_block(tmp_path, "docs", "| [A](a.md) | The A file |")
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.WARN
    assert "docs/b.md" in result.message


@pytest.mark.unit
@pytest.mark.ac("DINS-010")
def test_stale_embedded_block_broken_link(tmp_path: Path) -> None:
    """Covers: DINS-010"""
    _make_tree(tmp_path, "docs/a.md")
    _readme_with_block(
        tmp_path, "docs", "| [A](a.md) | The A file |", "| [Gone](gone.md) | Gone |"
    )
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.WARN
    assert "gone.md" in result.message


@pytest.mark.unit
@pytest.mark.ac("DINS-011")
def test_stale_index_md_wins_over_readme_block(tmp_path: Path) -> None:
    """Covers: DINS-011"""
    _make_tree(tmp_path, "docs/a.md")
    (tmp_path / "docs" / "INDEX.md").write_text("- [A](a.md)\n- [R](README.md)\n")
    _readme_with_block(tmp_path, "docs", "| [Nope](nope.md) | Not checked |")
    result = docs_index_stale.DocsIndexStale().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DISO-009")
def test_scope_embedded_block_deeper_path_warns(tmp_path: Path) -> None:
    """Covers: DISO-009"""
    _readme_with_block(tmp_path, "docs", "| [ADR](decisions/0001-x.md) | A decision |")
    result = docs_index_scope.DocsIndexScope().check(tmp_path)
    assert result.status == Status.WARN
    assert "docs/README.md -> decisions/0001-x.md" in result.message


@pytest.mark.unit
@pytest.mark.ac("DISO-010")
def test_scope_links_outside_block_are_ignored(tmp_path: Path) -> None:
    """Covers: DISO-010"""
    _readme_with_block(
        tmp_path,
        "docs",
        "| [A](a.md) | The A file |",
        prose="Read [the guide](../guide/start.md) first.\n",
    )
    result = docs_index_scope.DocsIndexScope().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("DISO-011")
def test_scope_embedded_block_child_readme_pointer_passes(tmp_path: Path) -> None:
    """Covers: DISO-011"""
    _readme_with_block(
        tmp_path, "docs", "| [Decisions](decisions/README.md) | ADR listing |"
    )
    result = docs_index_scope.DocsIndexScope().check(tmp_path)
    assert result.status == Status.PASS
