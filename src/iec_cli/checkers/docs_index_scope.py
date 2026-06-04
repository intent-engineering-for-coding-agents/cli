"""docs-index-scope — each INDEX.md maps only its own directory."""

import re
from pathlib import Path

from iec_cli.check import CheckResult, Severity, Status, registry
from iec_cli.checkers._shared import LINK_RE

_SUBDIR_INDEX_OR_README = re.compile(r"^[^/]+/(INDEX|README)\.md$")


def _is_in_scope(target: str) -> bool:
    """Return True if ``target`` is allowed inside an ``INDEX.md`` link table.

    Allowed:
      * Same-directory file — no ``/`` in the path.
      * Immediate child pointer — ``<subdir>/INDEX.md`` or ``<subdir>/README.md``.

    Anything else (deeper paths, ``../``, absolute URLs) is out of scope.
    Bare anchor fragments (``#section``) are treated as same-page references
    and allowed.
    """
    target = target.split("#", 1)[0]  # strip anchor fragment
    if not target:
        return True
    if "/" not in target:
        return True
    return bool(_SUBDIR_INDEX_OR_README.match(target))


@registry.register
class DocsIndexScope:
    id = "docs-index-scope"
    description = "Each INDEX.md maps only its own directory"

    def check(self, path: Path) -> CheckResult:
        docs_dir = path / "docs"
        if not docs_dir.is_dir():
            return CheckResult(
                self.id, Status.FAIL, "docs/ directory not found", Severity.HIGH
            )

        offenders: list[str] = []
        dirs = [docs_dir] + sorted(docs_dir.rglob("*"))
        for dirpath in dirs:
            if not dirpath.is_dir():
                continue
            index_file = dirpath / "INDEX.md"
            if not index_file.is_file():
                continue
            rel_dir = dirpath.relative_to(path).as_posix()
            for line in index_file.read_text(encoding="utf-8").splitlines():
                for match in LINK_RE.finditer(line):
                    target = match.group(2).strip()
                    if _is_in_scope(target):
                        continue
                    offenders.append(f"{rel_dir}/INDEX.md -> {target}")

        if not offenders:
            return CheckResult(
                self.id,
                Status.PASS,
                "All INDEX.md links stay within their own directory",
                Severity.MEDIUM,
            )
        return CheckResult(
            self.id,
            Status.WARN,
            f"Out-of-scope INDEX.md links: {', '.join(offenders)}",
            Severity.MEDIUM,
        )
