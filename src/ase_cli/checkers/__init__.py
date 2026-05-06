"""ASE deterministic checkers — each module registers itself on import."""

from ase_cli.checkers import (
    agents_exists,
    agents_links,
    agents_size,
    docs_index_exists,
    docs_index_stale,
    docs_readme_exists,
)

__all__ = [
    "agents_exists",
    "agents_links",
    "agents_size",
    "docs_index_exists",
    "docs_index_stale",
    "docs_readme_exists",
]
