"""spec-size — spec files under configurable line limit."""

import os
from pathlib import Path

from iec_cli.check import CheckResult, Severity, Status, registry
from iec_cli.checkers._shared import find_spec_files

_DEFAULT_LIMIT = 500


def _get_limit() -> int:
    try:
        return int(os.environ.get("ASE_SPEC_MAX_LINES", ""))
    except ValueError:
        return _DEFAULT_LIMIT


@registry.register
class SpecSize:
    id = "spec-size"
    description = "Spec files under configurable line limit (default 500)"

    def check(self, path: Path) -> CheckResult:
        spec_files = find_spec_files(path)
        if not spec_files:
            return CheckResult(
                self.id, Status.PASS, "No spec files found", Severity.MEDIUM
            )

        limit = _get_limit()
        violations: list[str] = []
        for spec_file in spec_files:
            line_count = len(spec_file.read_text(encoding="utf-8").splitlines())
            if line_count > limit:
                rel = spec_file.relative_to(path)
                violations.append(f"{rel} ({line_count} lines)")

        if not violations:
            return CheckResult(
                self.id,
                Status.PASS,
                f"All spec files within {limit}-line limit",
                Severity.MEDIUM,
            )
        return CheckResult(
            self.id,
            Status.WARN,
            f"{len(violations)} spec file(s) exceed {limit} lines: "
            f"{'; '.join(violations)}",
            Severity.MEDIUM,
        )
