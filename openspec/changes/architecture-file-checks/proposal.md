# Proposal: Architecture & File Structure Checks

## Why

Change 003 validates the single most critical AI-facing file (`AGENTS.md`). But ASE conventions require the entire `docs/` tree to be structured correctly: every subdirectory must have a `README.md` (human-facing overview, auto-renders on GitHub) and an `INDEX.md` (agent-facing file map). And every `INDEX.md` must stay in sync with actual files — a stale index misleads agents. These three recursive checkers close the gap.

## What Changes

- **`docs-readme-exists` checker**: Walks `docs/` recursively. Every subdirectory must contain a `README.md`. FAIL if any subdirectory is missing one.
- **`docs-index-exists` checker**: Walks `docs/` recursively. Every subdirectory should contain an `INDEX.md` (context economy optimization for agents). WARN if any subdirectory is missing one.
- **`docs-index-stale` checker**: For every `INDEX.md` found under `docs/`, parses file references and cross-references against actual files in that same directory. Reports broken links (referenced file missing) and orphan files (file present but not in INDEX). WARN for each mismatch.
- Each checker follows the same `Checker` protocol + `@registry.register` pattern.
- No modifications to existing specs.

## Capabilities

### New Capabilities

- `docs-readme-exists`: Recursively checks every `docs/` subdirectory has a `README.md`. FAIL if any missing.
- `docs-index-exists`: Recursively checks every `docs/` subdirectory has an `INDEX.md`. WARN if any missing.
- `docs-index-stale`: For each `INDEX.md` under `docs/`, cross-references its entries against files in that directory. WARN for broken links and orphan files. `.gitkeep` files are excluded from orphan detection.

### Modified Capabilities

*(None)*

## Impact

- **New modules**: `src/ase_cli/checkers/docs_readme_exists.py`, `docs_index_exists.py`, `docs_index_stale.py`
- **`src/ase_cli/checkers/__init__.py`**: Import new checker modules
- **Tests**: Unit tests with tmp_path directory trees, integration test against ase-cli's own `docs/`
- **No new dependencies**: Pure Python file I/O
