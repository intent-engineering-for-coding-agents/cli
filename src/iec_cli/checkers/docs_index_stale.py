"""docs-index-stale — cross-reference INDEX.md entries against actual files."""

from pathlib import Path

from iec_cli.check import CheckResult, Maturity, Severity, Status, registry
from iec_cli.checkers._shared import LINK_RE


@registry.register
class DocsIndexStale:
    id = "docs-index-stale"
    maturity = Maturity.ADVISORY
    description = "Cross-reference INDEX.md entries against actual files"

    def check(self, path: Path) -> CheckResult:
        docs_dir = path / "docs"
        if not docs_dir.is_dir():
            return CheckResult(
                self.id, Status.FAIL, "docs/ directory not found", Severity.HIGH
            )

        broken: list[str] = []
        orphans: list[str] = []

        dirs = [docs_dir] + sorted(docs_dir.rglob("*"))
        for dirpath in dirs:
            if not dirpath.is_dir():
                continue
            index_file = dirpath / "INDEX.md"
            if not index_file.is_file():
                continue

            # Gather all files in this directory (exclude .gitkeep and INDEX.md itself)
            actual_files: set[str] = set()
            for f in dirpath.iterdir():
                if f.is_file() and f.name != ".gitkeep" and f.name != "INDEX.md":
                    actual_files.add(f.name)

            # Parse referenced files from INDEX.md links
            referenced_names: set[str] = set()
            for line in index_file.read_text(encoding="utf-8").splitlines():
                match = LINK_RE.search(line)
                if not match:
                    continue
                ref_path = Path(match.group(2))
                if ref_path.is_absolute() or ref_path.parts[:1] == ("..",):
                    continue
                # Check if the referenced file exists relative to this INDEX dir
                full_path = (dirpath / ref_path).resolve()
                referenced_names.add(ref_path.name)
                if not full_path.is_file():
                    rel_dir = dirpath.relative_to(path).as_posix()
                    rel_ref = ref_path.as_posix()
                    broken.append(f"{rel_dir} -> {rel_ref}")

            # Orphans: on disk but not referenced
            for fname in sorted(actual_files):
                if fname not in referenced_names:
                    orphans.append(f"{dirpath.relative_to(path).as_posix()}/{fname}")

        if not broken and not orphans:
            return CheckResult(
                self.id, Status.PASS, "All INDEX files match filesystem", Severity.HIGH
            )

        parts: list[str] = []
        if broken:
            parts.append(f"Broken links: {', '.join(broken)}")
        if orphans:
            parts.append(f"Orphan files: {', '.join(orphans)}")
        return CheckResult(self.id, Status.WARN, "; ".join(parts), Severity.MEDIUM)
