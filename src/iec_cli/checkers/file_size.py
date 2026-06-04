"""file-size — .md files under configurable line limit."""

import os
from pathlib import Path

from iec_cli.check import CheckResult, Maturity, Severity, Status, registry

_DEFAULT_LIMIT = 500
_SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".vitepress"}


def _get_limit() -> int:
    try:
        return int(os.environ.get("ASE_FILE_MAX_LINES", ""))
    except ValueError:
        return _DEFAULT_LIMIT


def _md_files(path: Path) -> list[Path]:
    files: list[Path] = []
    for entry in path.rglob("*.md"):
        if entry.is_file() and not any(part in _SKIP_DIRS for part in entry.parts):
            files.append(entry)
    return sorted(files)


@registry.register
class FileSize:
    id = "file-size"
    maturity = Maturity.ADVISORY
    description = "All .md files under configurable line limit (default 500)"

    def check(self, path: Path) -> CheckResult:
        md_files = _md_files(path)
        if not md_files:
            return CheckResult(
                self.id, Status.PASS, "No .md files found", Severity.MEDIUM
            )

        limit = _get_limit()
        violations: list[str] = []
        for md_file in md_files:
            line_count = len(md_file.read_text(encoding="utf-8").splitlines())
            if line_count > limit:
                rel = md_file.relative_to(path)
                violations.append(f"{rel} ({line_count} lines)")

        if not violations:
            return CheckResult(
                self.id,
                Status.PASS,
                f"All .md files within {limit}-line limit",
                Severity.MEDIUM,
            )
        return CheckResult(
            self.id,
            Status.WARN,
            f"{len(violations)} .md file(s) exceed {limit} lines: "
            f"{'; '.join(violations)}",
            Severity.MEDIUM,
        )
