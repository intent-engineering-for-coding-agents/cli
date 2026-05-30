"""test-traceability — cross-reference spec AC IDs against test markers."""

import re
from pathlib import Path

from ase_cli.check import CheckResult, Severity, Status, registry
from ase_cli.checkers._shared import find_spec_files, find_test_files

_SCENARIO_SPLIT_RE = re.compile(r"(^#{3,6}\s+Scenario:\s+.+$)", re.MULTILINE)
_AC_ID_IN_HEADING_RE = re.compile(r"\[([A-Z][A-Z0-9]+-\d+)\]")
_MANUAL_RE = re.compile(r"Test-type:\s*Manual", re.IGNORECASE)

_MARKER_PATTERNS = [
    re.compile(r'@pytest\.mark\.ac\(\s*["\']([A-Z][A-Z0-9]+-\d+)["\']\s*\)'),
    re.compile(r'@Tag\(\s*["\']([A-Z][A-Z0-9]+-\d+)["\']\s*\)'),
    re.compile(r"@AC:([A-Z][A-Z0-9]+-\d+)"),
    re.compile(r"//\s*AC:\s*([A-Z][A-Z0-9]+-\d+)"),
]


def _collect_required_ids(path: Path) -> set[str]:
    """Return non-Manual AC IDs from spec scenario headings."""
    required: set[str] = set()
    for spec_file in find_spec_files(path):
        content = spec_file.read_text(encoding="utf-8")
        parts = _SCENARIO_SPLIT_RE.split(content)
        for i in range(1, len(parts), 2):
            heading = parts[i]
            body = parts[i + 1] if i + 1 < len(parts) else ""
            if _MANUAL_RE.search(body):
                continue
            m = _AC_ID_IN_HEADING_RE.search(heading)
            if m:
                required.add(m.group(1))
    return required


def _collect_marked_ids(path: Path) -> set[str]:
    """Return all AC IDs referenced by at least one test marker."""
    marked: set[str] = set()
    for test_file in find_test_files(path):
        content = test_file.read_text(encoding="utf-8", errors="replace")
        for pattern in _MARKER_PATTERNS:
            for m in pattern.finditer(content):
                marked.add(m.group(1))
    return marked


@registry.register
class TestTraceability:
    id = "test-traceability"
    description = "Every non-Manual spec AC ID has at least one test marker"

    def check(self, path: Path) -> CheckResult:
        required = _collect_required_ids(path)
        if not required:
            return CheckResult(
                self.id, Status.PASS, "No spec files found", Severity.HIGH
            )

        marked = _collect_marked_ids(path)
        uncovered = sorted(required - marked)
        orphaned = sorted(marked - required)

        if uncovered:
            parts = [
                f"{len(uncovered)} AC(s) have no test marker: {', '.join(uncovered)}"
            ]
            if orphaned:
                parts.append(f"orphaned markers: {', '.join(orphaned)}")
            return CheckResult(self.id, Status.FAIL, "; ".join(parts), Severity.HIGH)

        if orphaned:
            return CheckResult(
                self.id,
                Status.WARN,
                f"{len(orphaned)} orphaned test marker(s) (no matching spec AC): "
                f"{', '.join(orphaned)}",
                Severity.HIGH,
            )

        return CheckResult(
            self.id, Status.PASS, "All spec AC IDs have test markers", Severity.HIGH
        )
