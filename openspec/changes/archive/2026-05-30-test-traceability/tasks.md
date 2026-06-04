# Tasks: test-traceability (Change 009)

## 1. Shared helper

- [x] 1.1 Add `find_test_files(path)` to `src/iec_cli/checkers/_shared.py` — walks `tests/` (or `ASE_TESTS_DIR`) recursively, returns `.py` and `.feature` files

## 2. test-traceability — implementation

- [x] 2.1 Create `src/iec_cli/checkers/test_traceability.py` with `TestTraceability` class registered via `@registry.register`
- [x] 2.2 Implement `_collect_required_ids(path)` — scans spec files, extracts non-Manual AC IDs
- [x] 2.3 Implement `_collect_marked_ids(path)` — scans test files, extracts AC IDs from all four marker patterns

## 3. test-traceability — proof

- [x] 3.1 Positive: no spec files → PASS [TRTC-001]
- [x] 3.2 Positive: all ACs covered → PASS [TRTC-002]
- [x] 3.3 Negative: missing marker → FAIL with ID in message [TRTC-003]
- [x] 3.4 Negative: multiple missing → all reported [TRTC-004]
- [x] 3.5 Exemption: Manual AC not required [TRTC-005]
- [x] 3.6 Marker: pytest mark.ac() [TRTC-006]
- [x] 3.7 Marker: JUnit @Tag [TRTC-007]
- [x] 3.8 Marker: Cucumber @AC: [TRTC-008]
- [x] 3.9 Marker: inline comment [TRTC-009]
- [x] 3.10 Orphaned marker → WARN [TRTC-010]
- [x] 3.11 Registration [TRTC-011]

## 4. Wiring

- [x] 4.1 Import `test_traceability` in `src/iec_cli/checkers/__init__.py`
- [x] 4.2 Add `test-traceability` assertion to integration test

## 5. Verify

- [x] 5.1 `uv run ruff check` — no lint errors
- [x] 5.2 `uv run ruff format --check` — no formatting issues
- [x] 5.3 `uv run pytest -v` — all 11 TRTC ACs proven
