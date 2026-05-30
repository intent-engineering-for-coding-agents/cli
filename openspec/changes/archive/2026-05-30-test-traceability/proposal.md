## Why

Specs define AC IDs; tests are supposed to prove them. Without a cross-reference check, IDs can silently drift — a test marker may reference a removed AC ID or a spec scenario may have no test at all. `test-traceability` closes that gap deterministically.

## What Changes

- New checker `test-traceability` scans spec files for AC IDs and test files for matching markers, then reports any AC IDs that have no corresponding test marker.
- Supported marker formats: `@pytest.mark.<AC_ID>`, `@Tag("<AC_ID>")` (JUnit), `@AC:<AC_ID>` (Cucumber), `// AC: <AC_ID>` (inline comment fallback).
- AC IDs are collected from `Scenario:` headings in `openspec/specs/` and active change specs (excluding archive).
- Test files are discovered under a configurable `tests/` directory (default).

## Capabilities

### New Capabilities

- `test-traceability`: Cross-reference AC IDs from specs against test file markers; fail when any non-Manual AC ID has no test proof.

### Modified Capabilities

(none)

## Impact

- New file: `src/ase_cli/checkers/test_traceability.py`
- Update: `src/ase_cli/checkers/__init__.py`
- New test file: `tests/test_traceability_checker.py`
