## Design: test-traceability checker

### Approach

Single-module checker following the existing pattern in `checkers/`. Two
scan passes: collect AC IDs from specs, collect markers from tests, then
cross-reference.

### AC ID collection

Reuse `find_spec_files()` from `_shared.py` to get spec files. For each file:

1. Split on `Scenario:` headings using the regex already established in
   `spec_ac_ids.py` (`_SCENARIO_SPLIT_RE`).
2. Extract `[PREFIX-NNN]` from the heading line.
3. Check the scenario body for `Test-type: Manual` — if present, skip the ID.

Result: a set of non-Manual AC IDs that require proof.

### Marker collection

Walk `tests/` (or `ASE_TESTS_DIR` override) recursively. For `.py` and
`.feature` files, apply four regex patterns to each line:

```
@pytest.mark.ac\(\s*["']([A-Z][A-Z0-9]+-\d+)["']\s*\)
@Tag\(\s*["']([A-Z][A-Z0-9]+-\d+)["']\s*\)
@AC:([A-Z][A-Z0-9]+-\d+)
//\s*AC:\s*([A-Z][A-Z0-9]+-\d+)
```

Result: a set of AC IDs referenced by at least one test marker.

### Cross-reference logic

- `uncovered = required_ids - marked_ids` → non-empty → FAIL
- `orphaned = marked_ids - required_ids` → non-empty → WARN
- Both empty → PASS

When both uncovered and orphaned exist, FAIL takes precedence and both are
reported in the message.

### Module structure

```
src/ase_cli/checkers/test_traceability.py
  _SCENARIO_HEADING_RE   — matches #### Scenario: ... [ID]
  _AC_ID_RE              — extracts [PREFIX-NNN] from heading
  _MANUAL_RE             — matches Test-type: Manual in body
  _MARKER_PATTERNS       — list of compiled regexes for test markers
  _collect_required_ids(path) -> set[str]
  _collect_marked_ids(path) -> set[str]
  TestTraceability.check(path) -> CheckResult
```

### No tests/ directory

If `tests/` does not exist and required IDs is non-empty, `marked_ids` is
empty, so all required IDs are uncovered → FAIL. No special-case needed.
If required IDs is also empty (no specs), the `no spec files` early-return
fires first → PASS.
