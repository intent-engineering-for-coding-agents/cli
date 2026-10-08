"""docs-index-exists — verify every docs/ subdirectory has an index."""

from pathlib import Path

from iec_cli.check import CheckResult, Maturity, Severity, Status, registry
from iec_cli.checkers._shared import index_source, is_effectively_empty


@registry.register
class DocsIndexExists:
    id = "docs-index-exists"
    maturity = Maturity.ADVISORY
    description = "Every docs/ subdirectory has an INDEX.md or README.md index"

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
                and index_source(dirpath) is None
            ):
                missing.append(dirpath.relative_to(path).as_posix())

        if not missing:
            return CheckResult(
                self.id,
                Status.PASS,
                "All docs/ directories have an index",
                Severity.HIGH,
            )
        return CheckResult(
            self.id,
            Status.WARN,
            f"Missing index (INDEX.md or README.md block) in: {', '.join(missing)}",
            Severity.MEDIUM,
        )
