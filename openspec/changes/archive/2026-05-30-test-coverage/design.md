## Design: test-coverage checker

### Approach

Thin checker that reuses the helpers added by `test-traceability`. Rather than
collecting a set of marked IDs it needs a *count* per ID, so the shared helper
returns a `Counter` (or `dict[str, int]`) instead of a plain set.

### Shared helper update

`find_test_files(path)` is already added by Change 009. This change needs a
`collect_marker_counts(path) -> dict[str, int]` variant (or extend
`_collect_marked_ids` to return counts). The cleanest approach: add
`_collect_marker_counts` as a new internal function in `test_coverage.py`
that mirrors `_collect_marked_ids` but uses `Counter`.

Alternatively, expose it from `_shared.py` so both checkers can share it.
Given the two checkers are in separate modules and the logic is small, keeping
it local to each module avoids coupling.

### Cross-reference logic

```
required_ids  = non-Manual AC IDs from specs
marker_counts = { id: count } from test files (0 if absent)

under_covered = [id for id in required_ids
                 if 1 <= marker_counts.get(id, 0) < 2]
```

Note: IDs with `marker_counts == 0` are excluded (those belong to
`test-traceability`). This checker only warns about IDs that *have* coverage
but not enough of it.

- `under_covered` non-empty → WARN listing all IDs and their counts
- `under_covered` empty → PASS

### Module structure

```
src/ase_cli/checkers/test_coverage.py
  _collect_marker_counts(path) -> dict[str, int]
  TestCoverage.check(path) -> CheckResult
```
