"""change-archived — fail when a fully-completed change folder is not archived."""

from pathlib import Path

from iec_cli.check import CheckResult, Severity, Status, registry
from iec_cli.checkers.tasks_complete import _TASK_RE, _UNCHECKED_RE, _active_change_dirs


def _is_completed(tasks_file: Path) -> bool:
    """Return True when tasks.md has at least one task and zero unchecked items."""
    content = tasks_file.read_text(encoding="utf-8")
    if not _TASK_RE.search(content):
        return False
    return not _UNCHECKED_RE.search(content)


@registry.register
class ChangeArchived:
    id = "change-archived"
    description = (
        "Every fully-completed change folder has been archived "
        "(moved to openspec/changes/archive/)"
    )

    def check(self, path: Path) -> CheckResult:
        dirs = _active_change_dirs(path)
        unarchived: list[str] = []
        for change_dir in dirs:
            tasks_file = change_dir / "tasks.md"
            if not tasks_file.is_file():
                continue
            if _is_completed(tasks_file):
                unarchived.append(change_dir.name)

        if unarchived:
            names = ", ".join(sorted(unarchived))
            return CheckResult(
                self.id,
                Status.FAIL,
                f"{len(unarchived)} completed change folder(s) not yet archived:"
                f" {names}",
                Severity.HIGH,
            )

        return CheckResult(
            self.id,
            Status.PASS,
            "No unarchived completed change folders",
            Severity.HIGH,
        )
