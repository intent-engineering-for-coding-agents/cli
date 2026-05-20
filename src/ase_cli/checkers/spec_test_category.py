"""spec-test-category — every spec scenario section has a **Test:** field."""

import re
from pathlib import Path

from ase_cli.check import CheckResult, Severity, Status, registry
from ase_cli.checkers._shared import find_spec_files

_SCENARIO_SPLIT_RE = re.compile(r"(^#{3,6}\s+Scenario:\s+.+$)", re.MULTILINE)
_TEST_FIELD_RE = re.compile(r"^\*\*Test:\*\*", re.MULTILINE)


def _check_test_fields(content: str, rel_path: str) -> list[str]:
    """Return violation messages for scenarios missing a **Test:** field."""
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
    description = "Every spec scenario section has a **Test:** field"

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
                "All scenario sections have **Test:** field",
                Severity.HIGH,
            )
        return CheckResult(
            self.id,
            Status.FAIL,
            f"{len(violations)} scenario(s) missing **Test:** field: "
            f"{'; '.join(violations)}",
            Severity.HIGH,
        )
