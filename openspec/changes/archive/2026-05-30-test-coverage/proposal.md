## Why

`test-traceability` confirms that every non-Manual AC has at least one test marker.
That is necessary but not sufficient. A single test is not a proof strategy — the
convention requires both positive and negative coverage per AC. `test-coverage`
enforces the minimum pair requirement deterministically.

## What Changes

- New checker `test-coverage` warns when a non-Manual AC ID has fewer than 2 test
  markers referencing it (indicating likely missing positive or negative proof).
- Reuses the same spec-scanning and test-file-scanning helpers introduced by
  `test-traceability`.

## Capabilities

### New Capabilities

- `test-coverage`: For each non-Manual AC ID, assert that at least 2 test markers
  reference it; WARN when only 1 is found (proxy for missing positive or negative proof).

### Modified Capabilities

(none)

## Impact

- New file: `src/ase_cli/checkers/test_coverage.py`
- Update: `src/ase_cli/checkers/__init__.py`
- Extends `tests/test_traceability_checker.py` or new `tests/test_coverage_checker.py`
