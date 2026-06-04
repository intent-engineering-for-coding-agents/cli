"""adr-index — verify docs/decisions/README.md lists every ADR file."""

import re
from pathlib import Path

from iec_cli.check import CheckResult, Severity, Status, registry
from iec_cli.checkers._shared import LINK_RE

_ADR_FILENAME_RE = re.compile(r"^\d{4}-[a-z0-9-]+\.md$")


@registry.register
class AdrIndex:
    id = "adr-index"
    description = "Verify docs/decisions/README.md lists every ADR file"

    def check(self, path: Path) -> CheckResult:
        decisions_dir = path / "docs" / "decisions"
        if not decisions_dir.is_dir():
            return CheckResult(
                self.id, Status.PASS, "No docs/decisions/ directory", Severity.HIGH
            )

        adr_files = sorted(
            f.name
            for f in decisions_dir.iterdir()
            if f.is_file() and _ADR_FILENAME_RE.match(f.name)
        )

        if not adr_files:
            return CheckResult(
                self.id, Status.PASS, "No ADR files to index", Severity.HIGH
            )

        readme = decisions_dir / "README.md"
        if not readme.is_file():
            return CheckResult(
                self.id,
                Status.FAIL,
                "docs/decisions/README.md missing — ADRs present but not indexed",
                Severity.HIGH,
            )

        linked: set[str] = set()
        for line in readme.read_text(encoding="utf-8").splitlines():
            m = LINK_RE.search(line)
            if m:
                linked.add(Path(m.group(2)).name)

        unlisted = [f for f in adr_files if f not in linked]
        if not unlisted:
            return CheckResult(
                self.id,
                Status.PASS,
                "All ADRs are listed in README.md",
                Severity.HIGH,
            )
        return CheckResult(
            self.id,
            Status.FAIL,
            f"ADRs not listed in README.md: {', '.join(unlisted)}",
            Severity.HIGH,
        )
