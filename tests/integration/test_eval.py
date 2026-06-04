"""Integration tests for the `iec eval` CLI command."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from iec_cli.eval import eval_app
from iec_cli.main import app

runner = CliRunner()


def _write_checks(eval_dir: Path, task_name: str, yaml_content: str) -> Path:
    task_dir = eval_dir / task_name
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "checks.yaml").write_text(yaml_content)
    return task_dir


_SIMPLE_PASS_YAML = """\
checks:
  - id: readme
    description: readme exists
    type: file_exists
    path: README.md
"""

_SIMPLE_FAIL_YAML = """\
checks:
  - id: missing
    description: should not exist
    type: file_exists
    path: MISSING.md
"""

_MIXED_YAML = """\
checks:
  - id: pass-check
    description: exists
    type: file_exists
    path: EXISTS.md
  - id: fail-check
    description: missing
    type: file_exists
    path: MISSING.md
"""

_SMALL_YAML = """\
checks:
  - id: f
    description: x
    type: file_exists
    path: {filename}
"""


# ---------------------------------------------------------------------------
# No tasks
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-001")
def test_no_tasks_found(tmp_path: Path) -> None:
    result = runner.invoke(
        eval_app,
        ["--path", str(tmp_path), "--eval-dir", str(tmp_path / "eval")],
    )
    assert result.exit_code == 0
    assert "No eval tasks found" in result.stdout


# ---------------------------------------------------------------------------
# All pass
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-002")
@pytest.mark.ac("EVAL-014")
def test_all_pass_exit_zero_and_score(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Hello")
    eval_dir = tmp_path / "eval"
    _write_checks(eval_dir, "01-check", _SIMPLE_PASS_YAML)
    result = runner.invoke(
        eval_app,
        ["--path", str(tmp_path), "--eval-dir", str(eval_dir)],
    )
    assert result.exit_code == 0
    assert "1/1 (100%)" in result.stdout
    assert "Failures" not in result.stdout


# ---------------------------------------------------------------------------
# Failures
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-003")
@pytest.mark.ac("EVAL-016")
def test_one_failure_exit_two_and_failures_block(tmp_path: Path) -> None:
    eval_dir = tmp_path / "eval"
    _write_checks(eval_dir, "01-check", _SIMPLE_FAIL_YAML)
    result = runner.invoke(
        eval_app,
        ["--path", str(tmp_path), "--eval-dir", str(eval_dir)],
    )
    assert result.exit_code == 2
    assert "Failures:" in result.stdout
    assert "missing" in result.stdout


# ---------------------------------------------------------------------------
# Mixed results
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-004")
def test_mixed_results_table_counts(tmp_path: Path) -> None:
    (tmp_path / "EXISTS.md").write_text("exists")
    eval_dir = tmp_path / "eval"
    _write_checks(eval_dir, "01-mixed", _MIXED_YAML)
    result = runner.invoke(
        eval_app,
        ["--path", str(tmp_path), "--eval-dir", str(eval_dir)],
    )
    assert result.exit_code == 2
    assert "1/2" in result.stdout


# ---------------------------------------------------------------------------
# Flags
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-011")
def test_eval_dir_flag(tmp_path: Path) -> None:
    (tmp_path / "f.txt").write_text("hi")
    custom_eval = tmp_path / "my-evals"
    _write_checks(custom_eval, "01-t", _SMALL_YAML.format(filename="f.txt"))
    result = runner.invoke(
        eval_app,
        ["--path", str(tmp_path), "--eval-dir", str(custom_eval)],
    )
    assert result.exit_code == 0
    assert "100%" in result.stdout


@pytest.mark.ac("EVAL-012")
def test_path_flag_scopes_checks(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    (target / "README.md").write_text("hi")
    eval_dir = tmp_path / "eval"
    _write_checks(eval_dir, "01-t", _SIMPLE_PASS_YAML)
    result = runner.invoke(
        eval_app,
        ["--path", str(target), "--eval-dir", str(eval_dir)],
    )
    assert result.exit_code == 0
    assert "100%" in result.stdout


# ---------------------------------------------------------------------------
# Malformed YAML
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-010")
def test_malformed_yaml_shows_parse_error(tmp_path: Path) -> None:
    eval_dir = tmp_path / "eval"
    task_dir = eval_dir / "01-bad"
    task_dir.mkdir(parents=True)
    (task_dir / "checks.yaml").write_text("checks: [bad: yaml: !!: nope")
    result = runner.invoke(
        eval_app,
        ["--path", str(tmp_path), "--eval-dir", str(eval_dir)],
    )
    assert result.exit_code == 2
    assert "parse error" in result.stdout


# ---------------------------------------------------------------------------
# Warnings column present
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-015")
def test_warnings_column_present_in_output(tmp_path: Path) -> None:
    (tmp_path / "f.md").write_text("content")
    eval_dir = tmp_path / "eval"
    _write_checks(eval_dir, "01-t", _SMALL_YAML.format(filename="f.md"))
    result = runner.invoke(
        eval_app,
        ["--path", str(tmp_path), "--eval-dir", str(eval_dir)],
    )
    assert result.exit_code == 0
    assert "Warn" in result.stdout


# ---------------------------------------------------------------------------
# iec --help lists eval
# ---------------------------------------------------------------------------


@pytest.mark.ac("EVAL-017")
def test_ase_help_lists_eval() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "eval" in result.stdout
