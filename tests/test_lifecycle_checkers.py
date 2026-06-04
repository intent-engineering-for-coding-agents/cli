"""Unit tests for tasks-complete and change-archived checkers."""

from pathlib import Path

from iec_cli.check import Registry, Status
from iec_cli.checkers import change_archived, tasks_complete


def _write_tasks(base: Path, change_name: str, content: str) -> Path:
    tasks_file = base / "openspec" / "changes" / change_name / "tasks.md"
    tasks_file.parent.mkdir(parents=True, exist_ok=True)
    tasks_file.write_text(content)
    return tasks_file


# ---------------------------------------------------------------------------
# tasks-complete
# ---------------------------------------------------------------------------

_ALL_CHECKED = "# Tasks\n\n- [x] 1.1 first\n- [x] 1.2 second\n"
_HAS_UNCHECKED = "# Tasks\n\n- [x] 1.1 done\n- [ ] 1.2 not done\n"
_ALL_UNCHECKED = "# Tasks\n\n- [ ] 1.1 first\n- [ ] 1.2 second\n"


def test_tasks_complete_no_changes_dir(tmp_path: Path) -> None:
    """Covers: TSKC-001"""
    result = tasks_complete.TasksComplete().check(tmp_path)
    assert result.status == Status.PASS


def test_tasks_complete_no_tasks_files(tmp_path: Path) -> None:
    """Covers: TSKC-002"""
    (tmp_path / "openspec" / "changes" / "my-change").mkdir(parents=True)
    result = tasks_complete.TasksComplete().check(tmp_path)
    assert result.status == Status.PASS


def test_tasks_complete_all_checked(tmp_path: Path) -> None:
    """Covers: TSKC-003"""
    _write_tasks(tmp_path, "my-change", _ALL_CHECKED)
    result = tasks_complete.TasksComplete().check(tmp_path)
    assert result.status == Status.PASS


def test_tasks_complete_unchecked_item(tmp_path: Path) -> None:
    """Covers: TSKC-004"""
    _write_tasks(tmp_path, "my-change", _HAS_UNCHECKED)
    result = tasks_complete.TasksComplete().check(tmp_path)
    assert result.status == Status.FAIL
    assert "my-change" in result.message


def test_tasks_complete_multiple_incomplete(tmp_path: Path) -> None:
    """Covers: TSKC-005"""
    _write_tasks(tmp_path, "change-a", _HAS_UNCHECKED)
    _write_tasks(tmp_path, "change-b", _ALL_UNCHECKED)
    result = tasks_complete.TasksComplete().check(tmp_path)
    assert result.status == Status.FAIL
    assert "change-a" in result.message
    assert "change-b" in result.message


def test_tasks_complete_archive_skipped(tmp_path: Path) -> None:
    """Covers: TSKC-006"""
    archive_tasks = (
        tmp_path / "openspec" / "changes" / "archive" / "2026-01-01-old" / "tasks.md"
    )
    archive_tasks.parent.mkdir(parents=True, exist_ok=True)
    archive_tasks.write_text(_HAS_UNCHECKED)
    result = tasks_complete.TasksComplete().check(tmp_path)
    assert result.status == Status.PASS


def test_tasks_complete_registered() -> None:
    """Covers: TSKC-007"""
    reg = Registry()
    reg.register(tasks_complete.TasksComplete)
    assert "tasks-complete" in [c[0] for c in reg.list_all()]


# ---------------------------------------------------------------------------
# change-archived
# ---------------------------------------------------------------------------


def test_change_archived_no_changes_dir(tmp_path: Path) -> None:
    """Covers: CHGA-001"""
    result = change_archived.ChangeArchived().check(tmp_path)
    assert result.status == Status.PASS


def test_change_archived_no_active_folders(tmp_path: Path) -> None:
    """Covers: CHGA-002"""
    (tmp_path / "openspec" / "changes" / "archive").mkdir(parents=True)
    result = change_archived.ChangeArchived().check(tmp_path)
    assert result.status == Status.PASS


def test_change_archived_in_progress_not_flagged(tmp_path: Path) -> None:
    """Covers: CHGA-003"""
    _write_tasks(tmp_path, "my-change", _HAS_UNCHECKED)
    result = change_archived.ChangeArchived().check(tmp_path)
    assert result.status == Status.PASS


def test_change_archived_completed_not_archived(tmp_path: Path) -> None:
    """Covers: CHGA-004"""
    _write_tasks(tmp_path, "my-change", _ALL_CHECKED)
    result = change_archived.ChangeArchived().check(tmp_path)
    assert result.status == Status.FAIL
    assert "my-change" in result.message


def test_change_archived_multiple_completed(tmp_path: Path) -> None:
    """Covers: CHGA-005"""
    _write_tasks(tmp_path, "change-a", _ALL_CHECKED)
    _write_tasks(tmp_path, "change-b", _ALL_CHECKED)
    result = change_archived.ChangeArchived().check(tmp_path)
    assert result.status == Status.FAIL
    assert "change-a" in result.message
    assert "change-b" in result.message


def test_change_archived_no_tasks_file_not_flagged(tmp_path: Path) -> None:
    """Covers: CHGA-006"""
    (tmp_path / "openspec" / "changes" / "my-change").mkdir(parents=True)
    result = change_archived.ChangeArchived().check(tmp_path)
    assert result.status == Status.PASS


def test_change_archived_registered() -> None:
    """Covers: CHGA-007"""
    reg = Registry()
    reg.register(change_archived.ChangeArchived)
    assert "change-archived" in [c[0] for c in reg.list_all()]
