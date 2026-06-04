"""agents-links — verify links in AGENTS.md have descriptive text."""

import re
from pathlib import Path

from iec_cli.check import CheckResult, Severity, Status, registry

_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")


@registry.register
class AgentsLinks:
    id = "agents-links"
    description = "Verify links in AGENTS.md have descriptive text"

    def check(self, path: Path) -> CheckResult:
        agents_file = path / "AGENTS.md"
        if not agents_file.is_file():
            return CheckResult(
                self.id, Status.FAIL, "AGENTS.md not found", Severity.HIGH
            )

        bare_links: list[str] = []
        for line in agents_file.read_text(encoding="utf-8").splitlines():
            match = _LINK_RE.search(line)
            if not match:
                continue
            after_link = line[match.end() :].strip()
            if not after_link:
                bare_links.append(match.group(2))

        if not bare_links:
            return CheckResult(
                self.id, Status.PASS, "All links have descriptions", Severity.HIGH
            )
        return CheckResult(
            self.id,
            Status.WARN,
            f"Bare links found: {', '.join(bare_links)}",
            Severity.MEDIUM,
        )
