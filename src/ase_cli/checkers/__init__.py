"""ASE deterministic checkers — each module registers itself on import."""

from ase_cli.checkers import (
    adr_format,
    adr_index,
    agents_exists,
    agents_hub_structure,
    agents_links,
    agents_size,
    docs_index_exists,
    docs_index_scope,
    docs_index_stale,
    docs_readme_exists,
    file_size,
    secrets,
    spec_ac_ids,
    spec_size,
    spec_test_category,
)

__all__ = [
    "adr_format",
    "adr_index",
    "agents_exists",
    "agents_hub_structure",
    "agents_links",
    "agents_size",
    "docs_index_exists",
    "docs_index_scope",
    "docs_index_stale",
    "docs_readme_exists",
    "file_size",
    "secrets",
    "spec_ac_ids",
    "spec_size",
    "spec_test_category",
]
