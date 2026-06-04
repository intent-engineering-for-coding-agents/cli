"""tasks-complete — fail when an active change folder has unchecked tasks."""

import re
from pathlib import Path

from iec_cli.check import CheckResult, Severity, Status, registry

_UNCHECKED_RE = re.compile(r"^- \[ \]", re.MULTILINE)
_TASK_RE = re.compile(r"^- \[[ x]\]", re.MULTILINE | re.IGNORECASE)


def _active_change_dirs(path: Path) -> list[Path]:
    """Return direct subdirs of openspec/changes/ excluding archive/."""
    changes_dir = path / "openspec" / "changes"
    if not changes_dir.is_dir():
        return []
    return [d for d in changes_dir.iterdir() if d.is_dir() and d.name != "archive"]


@registry.register
class TasksComplete:
    id = "tasks-complete"
    description = "Every active change folder's tasks.md has no unchecked items"

    def check(self, path: Path) -> CheckResult:
        dirs = _active_change_dirs(path)
        incomplete: list[str] = []
        for change_dir in dirs:
            tasks_file = change_dir / "tasks.md"
            if not tasks_file.is_file():
                continue
            content = tasks_file.read_text(encoding="utf-8")
            if _UNCHECKED_RE.search(content):
                incomplete.append(change_dir.name)

        if incomplete:
            names = ", ".join(sorted(incomplete))
            return CheckResult(
                self.id,
                Status.FAIL,
                f"{len(incomplete)} change folder(s) have incomplete tasks: {names}",
                Severity.HIGH,
            )

        return CheckResult(
            self.id,
            Status.PASS,
            "No incomplete tasks in active change folders",
            Severity.HIGH,
        )
