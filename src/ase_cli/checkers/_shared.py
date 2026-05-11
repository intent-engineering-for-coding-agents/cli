"""Shared helpers for docs checkers."""

from pathlib import Path


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
