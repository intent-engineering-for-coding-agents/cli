"""agents-exists — verify AGENTS.md is present at repo root."""

from pathlib import Path

from iec_cli.check import CheckResult, Severity, Status, registry


@registry.register
class AgentsExists:
    id = "agents-exists"
    description = "Verify AGENTS.md exists at repo root"

    def check(self, path: Path) -> CheckResult:
        agents_file = path / "AGENTS.md"
        if agents_file.is_file():
            return CheckResult(self.id, Status.PASS, "AGENTS.md found", Severity.HIGH)
        return CheckResult(self.id, Status.FAIL, "AGENTS.md not found", Severity.HIGH)
