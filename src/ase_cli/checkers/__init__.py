"""ASE deterministic checkers — each module registers itself on import."""

from ase_cli.checkers import (
    adr_format,
    adr_index,
    agents_exists,
    agents_links,
    agents_size,
    docs_index_exists,
    docs_index_scope,
    docs_index_stale,
    docs_readme_exists,
    spec_ac_ids,
    spec_test_category,
)

__all__ = [
    "adr_format",
    "adr_index",
    "agents_exists",
    "agents_links",
    "agents_size",
    "docs_index_exists",
    "docs_index_scope",
    "docs_index_stale",
    "docs_readme_exists",
    "spec_ac_ids",
    "spec_test_category",
]
