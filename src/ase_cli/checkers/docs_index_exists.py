"""docs-index-exists — verify every docs/ subdirectory has an INDEX.md."""

from pathlib import Path

from ase_cli.check import CheckResult, Severity, Status, registry


@registry.register
class DocsIndexExists:
    id = "docs-index-exists"
    description = "Verify every docs/ subdirectory has an INDEX.md"

    def check(self, path: Path) -> CheckResult:
        docs_dir = path / "docs"
        if not docs_dir.is_dir():
            return CheckResult(
                self.id, Status.FAIL, "docs/ directory not found", Severity.HIGH
            )

        missing: list[str] = []
        dirs = [docs_dir] + sorted(docs_dir.rglob("*"))
        for dirpath in dirs:
            if dirpath.is_dir() and not (dirpath / "INDEX.md").is_file():
                missing.append(dirpath.relative_to(path).as_posix())

        if not missing:
            return CheckResult(
                self.id,
                Status.PASS,
                "All docs/ directories have INDEX.md",
                Severity.HIGH,
            )
        return CheckResult(
            self.id,
            Status.WARN,
            f"Missing INDEX.md in: {', '.join(missing)}",
            Severity.MEDIUM,
        )
