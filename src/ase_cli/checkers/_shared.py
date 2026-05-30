"""Shared helpers for docs checkers."""

import os
import re
from collections import Counter
from pathlib import Path

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
"""Match Markdown inline links — group 1 = text, group 2 = target."""

# ---------------------------------------------------------------------------
# Spec / AC ID parsing constants (shared by test-traceability and test-coverage)
# ---------------------------------------------------------------------------

SCENARIO_SPLIT_RE = re.compile(r"(^#{3,6}\s+Scenario:\s+.+$)", re.MULTILINE)
AC_ID_IN_HEADING_RE = re.compile(r"\[([A-Z][A-Z0-9]+-\d+)\]")
MANUAL_RE = re.compile(r"Test-type:\s*Manual", re.IGNORECASE)

MARKER_PATTERNS = [
    re.compile(r'@pytest\.mark\.ac\(\s*["\']([A-Z][A-Z0-9]+-\d+)["\']\s*\)'),
    re.compile(r'@Tag\(\s*["\']([A-Z][A-Z0-9]+-\d+)["\']\s*\)'),
    re.compile(r"@AC:([A-Z][A-Z0-9]+-\d+)"),
    re.compile(r"//\s*AC:\s*([A-Z][A-Z0-9]+-\d+)"),
]


def find_spec_files(path: Path) -> list[Path]:
    """Return all spec .md files under openspec/, excluding archived changes."""
    files: list[Path] = []
    specs_dir = path / "openspec" / "specs"
    if specs_dir.is_dir():
        files.extend(f for f in specs_dir.rglob("*.md") if f.is_file())
    changes_dir = path / "openspec" / "changes"
    if changes_dir.is_dir():
        for change_dir in changes_dir.iterdir():
            if change_dir.is_dir() and change_dir.name != "archive":
                spec_subdir = change_dir / "specs"
                if spec_subdir.is_dir():
                    files.extend(f for f in spec_subdir.rglob("*.md") if f.is_file())
    return sorted(files)


def find_test_files(path: Path) -> list[Path]:
    """Return test files under the tests/ directory.

    The directory defaults to ``<path>/tests`` but can be overridden via the
    ``ASE_TESTS_DIR`` environment variable (absolute or relative to ``path``).
    """
    tests_dir_name = os.environ.get("ASE_TESTS_DIR", "tests")
    tests_dir = Path(tests_dir_name)
    if not tests_dir.is_absolute():
        tests_dir = path / tests_dir
    if not tests_dir.is_dir():
        return []
    extensions = {".py", ".feature", ".java", ".kt", ".go", ".ts", ".js"}
    return sorted(
        f for f in tests_dir.rglob("*") if f.is_file() and f.suffix in extensions
    )


def collect_required_ids(path: Path) -> set[str]:
    """Return non-Manual AC IDs from spec scenario headings."""
    required: set[str] = set()
    for spec_file in find_spec_files(path):
        content = spec_file.read_text(encoding="utf-8")
        parts = SCENARIO_SPLIT_RE.split(content)
        for i in range(1, len(parts), 2):
            heading = parts[i]
            body = parts[i + 1] if i + 1 < len(parts) else ""
            if MANUAL_RE.search(body):
                continue
            m = AC_ID_IN_HEADING_RE.search(heading)
            if m:
                required.add(m.group(1))
    return required


def collect_marker_counts(path: Path) -> Counter[str]:
    """Return the number of test files that reference each AC ID.

    Each AC ID is counted at most once per file, regardless of how many
    marker formats match it in that file.
    """
    counts: Counter[str] = Counter()
    for test_file in find_test_files(path):
        content = test_file.read_text(encoding="utf-8", errors="replace")
        file_ids: set[str] = set()
        for pattern in MARKER_PATTERNS:
            for m in pattern.finditer(content):
                file_ids.add(m.group(1))
        counts.update(file_ids)
    return counts


def is_effectively_empty(dirpath: Path) -> bool:
    """True if dirpath has no substantive content anywhere below it.

    Entries whose name starts with ``.`` are ignored at every depth
    (``.gitkeep``, ``.hidden``, ``.DS_Store``...). A directory whose subtree
    contains only dotfiles or further empty directories is treated as a
    placeholder and skipped by presence checks.
    """
    for entry in dirpath.rglob("*"):
        if entry.is_file() and not entry.name.startswith("."):
            return False
    return True
