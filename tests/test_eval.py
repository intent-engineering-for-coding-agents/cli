"""Unit tests for iec eval — EvalCheck, _run_check."""

from pathlib import Path

import pytest

from iec_cli.check import Severity, Status
from iec_cli.eval import EvalCheck, _load_tasks, _run_check

# ---------------------------------------------------------------------------
# file_exists
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-008")
def test_file_exists_pass(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Hello")
    check = EvalCheck(id="readme", description="", type="file_exists", path="README.md")
    result = _run_check(check, tmp_path)
    assert result.status == Status.PASS
    assert result.check_id == "readme"


@pytest.mark.ac("EVAL-008")
def test_file_exists_fail(tmp_path: Path) -> None:
    check = EvalCheck(id="readme", description="", type="file_exists", path="README.md")
    result = _run_check(check, tmp_path)
    assert result.status == Status.FAIL


@pytest.mark.ac("EVAL-008")
def test_file_exists_glob_pass(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "INDEX.md").write_text("# Index")
    check = EvalCheck(id="idx", description="", type="file_exists", path="docs/*.md")
    result = _run_check(check, tmp_path)
    assert result.status == Status.PASS


@pytest.mark.ac("EVAL-008")
def test_file_exists_glob_fail(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    check = EvalCheck(id="idx", description="", type="file_exists", path="docs/*.md")
    result = _run_check(check, tmp_path)
    assert result.status == Status.FAIL


# ---------------------------------------------------------------------------
# directory_exists
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-009")
def test_directory_exists_pass(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    check = EvalCheck(id="src", description="", type="directory_exists", path="src")
    result = _run_check(check, tmp_path)
    assert result.status == Status.PASS


@pytest.mark.ac("EVAL-009")
def test_directory_exists_fail(tmp_path: Path) -> None:
    check = EvalCheck(id="src", description="", type="directory_exists", path="src")
    result = _run_check(check, tmp_path)
    assert result.status == Status.FAIL


# ---------------------------------------------------------------------------
# file_contains
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-005")
def test_file_contains_pass(tmp_path: Path) -> None:
    (tmp_path / "svc.py").write_text("class UserService:\n    pass\n")
    check = EvalCheck(
        id="has-class",
        description="",
        type="file_contains",
        file="svc.py",
        pattern="^class ",
    )
    result = _run_check(check, tmp_path)
    assert result.status == Status.PASS


@pytest.mark.ac("EVAL-006")
def test_file_contains_fail(tmp_path: Path) -> None:
    (tmp_path / "svc.py").write_text("def create():\n    pass\n")
    check = EvalCheck(
        id="has-class",
        description="",
        type="file_contains",
        file="svc.py",
        pattern="^class ",
    )
    result = _run_check(check, tmp_path)
    assert result.status == Status.FAIL
    assert "svc.py" in result.message


@pytest.mark.ac("EVAL-005")
def test_file_contains_multiline_anchor(tmp_path: Path) -> None:
    """^ must anchor to line starts, not just the start of the whole string."""
    content = "# header\nclass Foo:\n    pass\n"
    (tmp_path / "svc.py").write_text(content)
    check = EvalCheck(
        id="has-class",
        description="",
        type="file_contains",
        file="svc.py",
        pattern="^class ",
    )
    result = _run_check(check, tmp_path)
    assert result.status == Status.PASS


@pytest.mark.ac("EVAL-005")
def test_file_contains_missing_file(tmp_path: Path) -> None:
    check = EvalCheck(
        id="has-class",
        description="",
        type="file_contains",
        file="missing.py",
        pattern="^class ",
    )
    result = _run_check(check, tmp_path)
    assert result.status == Status.FAIL
    assert "not found" in result.message


# ---------------------------------------------------------------------------
# file_not_contains
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-007")
def test_file_not_contains_pass(tmp_path: Path) -> None:
    (tmp_path / "chapter.md").write_text("## Section\nSome text.\n")
    check = EvalCheck(
        id="no-h4",
        description="",
        type="file_not_contains",
        file="chapter.md",
        pattern="^####",
    )
    result = _run_check(check, tmp_path)
    assert result.status == Status.PASS


@pytest.mark.ac("EVAL-007")
def test_file_not_contains_fail(tmp_path: Path) -> None:
    (tmp_path / "chapter.md").write_text("## Section\n#### Deep heading\n")
    check = EvalCheck(
        id="no-h4",
        description="",
        type="file_not_contains",
        file="chapter.md",
        pattern="^####",
    )
    result = _run_check(check, tmp_path)
    assert result.status == Status.FAIL


# ---------------------------------------------------------------------------
# unknown type
# ---------------------------------------------------------------------------


def test_unknown_check_type(tmp_path: Path) -> None:
    check = EvalCheck(id="x", description="", type="file_grep")
    result = _run_check(check, tmp_path)
    assert result.status == Status.FAIL
    assert "unknown check type" in result.message


# ---------------------------------------------------------------------------
# severity default
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-013")
def test_severity_default_is_high(tmp_path: Path) -> None:
    (tmp_path / "f.md").write_text("content")
    check = EvalCheck(id="x", description="", type="file_exists", path="f.md")
    assert check.severity == Severity.HIGH
    result = _run_check(check, tmp_path)
    assert result.severity == Severity.HIGH


# ---------------------------------------------------------------------------
# _load_tasks
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-010")
def test_load_tasks_malformed_yaml(tmp_path: Path) -> None:
    task_dir = tmp_path / "01-bad"
    task_dir.mkdir()
    (task_dir / "checks.yaml").write_text("checks: [bad: yaml: !!: nope")
    pairs = _load_tasks(tmp_path)
    assert len(pairs) == 1
    task, results = pairs[0]
    assert task.name == "01-bad"
    assert len(results) == 1
    assert results[0].status == Status.FAIL
    assert "parse error" in results[0].message


def test_load_tasks_sorted(tmp_path: Path) -> None:
    for name in ("03-c", "01-a", "02-b"):
        d = tmp_path / name
        d.mkdir()
        (d / "checks.yaml").write_text("checks: []")
    pairs = _load_tasks(tmp_path)
    assert [t.name for t, _ in pairs] == ["01-a", "02-b", "03-c"]


def test_load_tasks_skips_non_dirs(tmp_path: Path) -> None:
    (tmp_path / "readme.md").write_text("# hi")
    task_dir = tmp_path / "01-ok"
    task_dir.mkdir()
    (task_dir / "checks.yaml").write_text("checks: []")
    pairs = _load_tasks(tmp_path)
    assert len(pairs) == 1


def test_load_tasks_skips_dirs_without_checks_yaml(tmp_path: Path) -> None:
    (tmp_path / "01-no-checks").mkdir()
    pairs = _load_tasks(tmp_path)
    assert len(pairs) == 0


def test_load_tasks_empty_dir(tmp_path: Path) -> None:
    pairs = _load_tasks(tmp_path)
    assert pairs == []


def test_load_tasks_missing_dir(tmp_path: Path) -> None:
    pairs = _load_tasks(tmp_path / "nonexistent")
    assert pairs == []
