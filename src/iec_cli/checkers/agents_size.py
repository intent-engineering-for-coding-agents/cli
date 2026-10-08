"""agents-size — verify AGENTS.md is under the line limit."""

import os
from pathlib import Path

from iec_cli.check import CheckResult, Maturity, Severity, Status, registry
from iec_cli.checkers._shared import front_matter_length

DEFAULT_MAX_LINES = 50


@registry.register
class AgentsSize:
    id = "agents-size"
    maturity = Maturity.CI
    description = "Verify AGENTS.md is under the line limit"

    def check(self, path: Path) -> CheckResult:
        agents_file = path / "AGENTS.md"
        if not agents_file.is_file():
            return CheckResult(
                self.id, Status.FAIL, "AGENTS.md not found", Severity.HIGH
            )

        max_lines = DEFAULT_MAX_LINES
        env_val = os.environ.get("ASE_AGENTS_MAX_LINES", "")
        if env_val:
            try:
                max_lines = int(env_val)
            except ValueError:
                pass

        lines = agents_file.read_text(encoding="utf-8").splitlines()
        header = front_matter_length(lines)
        line_count = len(lines) - header
        excluded = f" excluding {header} front matter lines" if header else ""
        if line_count <= max_lines:
            return CheckResult(
                self.id,
                Status.PASS,
                f"AGENTS.md is {line_count} lines{excluded} (limit: {max_lines})",
                Severity.HIGH,
            )
        return CheckResult(
            self.id,
            Status.FAIL,
            f"AGENTS.md has {line_count} lines{excluded} (limit: {max_lines})",
            Severity.HIGH,
        )
