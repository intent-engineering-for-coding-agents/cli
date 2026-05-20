# Proposal: File and Spec Size Checks

## Why

Oversized spec files lose agent focus — specs over ~500 lines start drifting. Oversized documentation files compound cognitive debt. Neither is caught by existing checks. These two advisory checks flag files that warrant splitting before they become a maintenance burden.

## What Changes

- **`spec-size` checker**: Walks the same spec files as `spec-ac-ids`. Returns WARN for any spec file exceeding the configurable line limit (default 500, env `ASE_SPEC_MAX_LINES`).
- **`file-size` checker**: Walks all `.md` files in the repo, skipping `.git/`, `node_modules/`, `.venv/`, `.vitepress/`, and `__pycache__/`. Returns WARN for any file exceeding the configurable line limit (default 500, env `ASE_FILE_MAX_LINES`).
- Both return WARN (advisory), not FAIL. Size is a smell, not a violation.

## Capabilities

### New Capabilities

- `spec-size`: Warns when a spec file exceeds the line limit. Configurable via `ASE_SPEC_MAX_LINES`.
- `file-size`: Warns when any `.md` file exceeds the line limit. Configurable via `ASE_FILE_MAX_LINES`.

### Modified Capabilities

*(None)*

## Impact

- **New modules**: `src/ase_cli/checkers/spec_size.py`, `src/ase_cli/checkers/file_size.py`
- **Updated**: `src/ase_cli/checkers/__init__.py`
- **Tests**: 13 unit tests (SPSZ-001..006, FLSZ-001..007)
- **No new dependencies**
