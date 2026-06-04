"""agents-hub-structure — .agents/ has instructions/ and skills/ subdirectories."""

from pathlib import Path

from iec_cli.check import CheckResult, Maturity, Severity, Status, registry


@registry.register
class AgentsHubStructure:
    id = "agents-hub-structure"
    maturity = Maturity.CI
    description = "Verify .agents/ hub has instructions/ and skills/ subdirectories"

    def check(self, path: Path) -> CheckResult:
        agents_dir = path / ".agents"
        if not agents_dir.is_dir():
            return CheckResult(
                self.id, Status.FAIL, ".agents/ directory not found", Severity.HIGH
            )

        missing = []
        if not (agents_dir / "instructions").is_dir():
            missing.append("instructions/")
        if not (agents_dir / "skills").is_dir():
            missing.append("skills/")

        if not missing:
            return CheckResult(
                self.id,
                Status.PASS,
                ".agents/ has instructions/ and skills/ subdirectories",
                Severity.HIGH,
            )
        return CheckResult(
            self.id,
            Status.FAIL,
            f".agents/ missing subdirectories: {', '.join(missing)}",
            Severity.HIGH,
        )
