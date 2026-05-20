"""Shared helpers for docs checkers."""

import re
from pathlib import Path

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
"""Match Markdown inline links — group 1 = text, group 2 = target."""


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
