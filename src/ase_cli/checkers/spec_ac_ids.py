"""spec-ac-ids — every spec scenario heading has a [PREFIX-NNN] AC ID."""

import re
from pathlib import Path

from ase_cli.check import CheckResult, Severity, Status, registry
from ase_cli.checkers._shared import find_spec_files

_SCENARIO_RE = re.compile(r"^#{3,6}\s+Scenario:\s+.+$", re.MULTILINE)
_AC_ID_RE = re.compile(r"\[[A-Z][A-Z0-9]+-\d+\]")


@registry.register
class SpecAcIds:
    id = "spec-ac-ids"
    description = "Every spec scenario heading has a [PREFIX-NNN] AC ID"

    def check(self, path: Path) -> CheckResult:
        spec_files = find_spec_files(path)
        if not spec_files:
            return CheckResult(
                self.id, Status.PASS, "No spec files found", Severity.HIGH
            )

        violations: list[str] = []
        for spec_file in spec_files:
            content = spec_file.read_text(encoding="utf-8")
            for match in _SCENARIO_RE.finditer(content):
                heading = match.group(0)
                if not _AC_ID_RE.search(heading):
                    rel = spec_file.relative_to(path)
                    violations.append(f"{rel}: {heading.strip()}")

        if not violations:
            return CheckResult(
                self.id, Status.PASS, "All scenario headings have AC IDs", Severity.HIGH
            )
        return CheckResult(
            self.id,
            Status.FAIL,
            f"{len(violations)} scenario(s) missing AC ID: {'; '.join(violations)}",
            Severity.HIGH,
        )
