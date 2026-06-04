"""test-traceability — cross-reference spec AC IDs against test markers."""

from pathlib import Path

from iec_cli.check import CheckResult, Maturity, Severity, Status, registry
from iec_cli.checkers._shared import (
    collect_marker_counts,
    collect_required_ids,
    find_spec_files,
)


@registry.register
class TestTraceability:
    id = "test-traceability"
    maturity = Maturity.CI
    description = "Every non-Manual spec AC ID has at least one test marker"

    def check(self, path: Path) -> CheckResult:
        if not find_spec_files(path):
            return CheckResult(
                self.id, Status.PASS, "No spec files found", Severity.HIGH
            )

        required = collect_required_ids(path)
        if not required:
            return CheckResult(
                self.id,
                Status.PASS,
                "No automation-required ACs found",
                Severity.HIGH,
            )

        marked = set(collect_marker_counts(path).keys())
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
