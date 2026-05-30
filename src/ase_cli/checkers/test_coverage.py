"""test-coverage — warn when a non-Manual AC has fewer than 2 test markers."""

from collections import Counter
from pathlib import Path

from ase_cli.check import CheckResult, Severity, Status, registry
from ase_cli.checkers._shared import find_spec_files, find_test_files
from ase_cli.checkers.test_traceability import (
    _AC_ID_IN_HEADING_RE,
    _MANUAL_RE,
    _MARKER_PATTERNS,
    _SCENARIO_SPLIT_RE,
)


def _collect_required_ids(path: Path) -> set[str]:
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


def _collect_marker_counts(path: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    for test_file in find_test_files(path):
        content = test_file.read_text(encoding="utf-8", errors="replace")
        for pattern in _MARKER_PATTERNS:
            for m in pattern.finditer(content):
                counts[m.group(1)] += 1
    return counts


@registry.register
class TestCoverage:
    id = "test-coverage"
    description = (
        "Every non-Manual spec AC ID has at least 2 test markers (positive + negative)"
    )

    def check(self, path: Path) -> CheckResult:
        required = _collect_required_ids(path)
        if not required:
            return CheckResult(
                self.id, Status.PASS, "No spec files found", Severity.MEDIUM
            )

        counts = _collect_marker_counts(path)
        under_covered = sorted(
            ac_id for ac_id in required if 1 <= counts.get(ac_id, 0) < 2
        )

        if under_covered:
            details = ", ".join(f"{ac}(1)" for ac in under_covered)
            return CheckResult(
                self.id,
                Status.WARN,
                f"{len(under_covered)} AC(s) have only 1 test marker (need 2+): "
                f"{details}",
                Severity.MEDIUM,
            )

        return CheckResult(
            self.id,
            Status.PASS,
            "All covered non-Manual ACs have 2+ test markers",
            Severity.MEDIUM,
        )
