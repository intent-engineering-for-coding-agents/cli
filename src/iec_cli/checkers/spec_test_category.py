"""spec-test-category — every spec scenario section has a Test-type: field."""

import re
from pathlib import Path

from iec_cli.check import CheckResult, Severity, Status, registry
from iec_cli.checkers._shared import find_spec_files

_SCENARIO_SPLIT_RE = re.compile(r"(^#{3,6}\s+Scenario:\s+.+$)", re.MULTILINE)
_TEST_FIELD_RE = re.compile(r"^Test-type:", re.MULTILINE)


def _check_test_fields(content: str, rel_path: str) -> list[str]:
    """Return violation messages for scenarios missing a Test-type: field."""
    parts = _SCENARIO_SPLIT_RE.split(content)
    violations = []
    # parts alternates: [pre, heading1, body1, heading2, body2, ...]
    for i in range(1, len(parts), 2):
        heading = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        if not _TEST_FIELD_RE.search(body):
            violations.append(f"{rel_path}: {heading.strip()}")
    return violations


@registry.register
class SpecTestCategory:
    id = "spec-test-category"
    description = "Every spec scenario section has a Test-type: field"

    def check(self, path: Path) -> CheckResult:
        spec_files = find_spec_files(path)
        if not spec_files:
            return CheckResult(
                self.id, Status.PASS, "No spec files found", Severity.HIGH
            )

        violations: list[str] = []
        for spec_file in spec_files:
            content = spec_file.read_text(encoding="utf-8")
            rel = str(spec_file.relative_to(path))
            violations.extend(_check_test_fields(content, rel))

        if not violations:
            return CheckResult(
                self.id,
                Status.PASS,
                "All scenario sections have Test-type: field",
                Severity.HIGH,
            )
        return CheckResult(
            self.id,
            Status.FAIL,
            f"{len(violations)} scenario(s) missing Test-type: field: "
            f"{'; '.join(violations)}",
            Severity.HIGH,
        )
