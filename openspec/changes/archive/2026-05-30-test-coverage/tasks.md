# Tasks: test-coverage (Change 010)

## 1. test-coverage — implementation

- [x] 1.1 Create `src/ase_cli/checkers/test_coverage.py` with `TestCoverage` class registered via `@registry.register`
- [x] 1.2 Implement `_collect_marker_counts(path)` — returns `dict[str, int]` of AC ID → marker count, reusing marker patterns from `test_traceability`

## 2. test-coverage — proof

- [x] 2.1 Positive: no spec files → PASS [TCOV-001]
- [x] 2.2 Positive: all ACs have 2+ markers → PASS [TCOV-002]
- [x] 2.3 Negative: AC with exactly 1 marker → WARN with ID in message [TCOV-003]
- [x] 2.4 Negative: multiple under-covered ACs → all reported [TCOV-004]
- [x] 2.5 Exemption: Manual AC not subject to count check [TCOV-005]
- [x] 2.6 AC with 0 markers → PASS (not double-reported) [TCOV-006]
- [x] 2.7 Registration [TCOV-007]

## 3. Wiring

- [x] 3.1 Import `test_coverage` in `src/ase_cli/checkers/__init__.py`
- [x] 3.2 Add `test-coverage` assertion to integration test

## 4. Verify

- [x] 4.1 `uv run ruff check` — no lint errors
- [x] 4.2 `uv run ruff format --check` — no formatting issues
- [x] 4.3 `uv run pytest -v` — all 7 TCOV ACs proven
