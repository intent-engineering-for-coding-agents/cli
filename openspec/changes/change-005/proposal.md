## Why

ADRs are a cornerstone ASE document type, but nothing currently prevents malformed filenames, missing required sections, or a stale index. Without format enforcement, agents may fail to find or parse decisions correctly. This change adds two deterministic checks to verify ADR structure and index completeness.

## What Changes

- Add `adr-format` checker: validates that every `.md` file in `docs/decisions/` matches the MADR filename convention and contains required section headings and a valid status line.
- Add `adr-index` checker: validates that `docs/decisions/README.md` exists and lists every ADR file present in that directory.

## Capabilities

### New Capabilities
- `adr-format`: Validates ADR filenames (`NNNN-kebab-case.md`), required MADR headings, and status values for all files in `docs/decisions/`.
- `adr-index`: Validates that `docs/decisions/README.md` exists and contains an entry for every ADR file in the directory.

### Modified Capabilities

_(none)_

## Impact

- `src/ase_cli/checkers/` — two new checker modules (`adr_format.py`, `adr_index.py`)
- `src/ase_cli/checkers/__init__.py` — import new modules to trigger registration
- `tests/` — new test files for each checker
- No changes to existing checkers or CLI interface
