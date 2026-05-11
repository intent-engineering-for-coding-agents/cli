"""docs-readme-exists — verify every docs/ subdirectory has a README.md."""

from pathlib import Path

from ase_cli.check import CheckResult, Severity, Status, registry
from ase_cli.checkers._shared import is_effectively_empty


@registry.register
class DocsReadmeExists:
    id = "docs-readme-exists"
    description = "Verify every docs/ subdirectory has a README.md"

    def check(self, path: Path) -> CheckResult:
        docs_dir = path / "docs"
        if not docs_dir.is_dir():
            return CheckResult(
                self.id, Status.FAIL, "docs/ directory not found", Severity.HIGH
            )

        missing: list[str] = []
        dirs = [docs_dir] + sorted(docs_dir.rglob("*"))
        for dirpath in dirs:
            if (
                dirpath.is_dir()
                and not is_effectively_empty(dirpath)
                and not (dirpath / "README.md").is_file()
            ):
                missing.append(dirpath.relative_to(path).as_posix())

        if not missing:
            return CheckResult(
                self.id,
                Status.PASS,
                "All docs/ directories have README.md",
                Severity.HIGH,
            )
        return CheckResult(
            self.id,
            Status.FAIL,
            f"Missing README.md in: {', '.join(missing)}",
            Severity.HIGH,
        )
