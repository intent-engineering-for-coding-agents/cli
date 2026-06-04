"""test-coverage — warn when a non-Manual AC has fewer than 2 test markers."""

from pathlib import Path

from iec_cli.check import CheckResult, Severity, Status, registry
from iec_cli.checkers._shared import (
    collect_marker_counts,
    collect_required_ids,
    find_spec_files,
)


@registry.register
class TestCoverage:
    id = "test-coverage"
    description = (
        "Every non-Manual spec AC ID has at least 2 test markers (positive + negative)"
    )

    def check(self, path: Path) -> CheckResult:
        if not find_spec_files(path):
            return CheckResult(
                self.id, Status.PASS, "No spec files found", Severity.MEDIUM
            )

        required = collect_required_ids(path)
        if not required:
            return CheckResult(
                self.id,
                Status.PASS,
                "No automation-required ACs found",
                Severity.MEDIUM,
            )

        counts = collect_marker_counts(path)
        under_covered = sorted(ac_id for ac_id in required if counts.get(ac_id, 0) < 2)

        if under_covered:
            details = ", ".join(f"{ac}({counts.get(ac, 0)})" for ac in under_covered)
            return CheckResult(
                self.id,
                Status.WARN,
                f"{len(under_covered)} AC(s) have fewer than 2 test markers: {details}",
                Severity.MEDIUM,
            )

        return CheckResult(
            self.id,
            Status.PASS,
            "All non-Manual ACs have 2+ test markers",
            Severity.MEDIUM,
        )
