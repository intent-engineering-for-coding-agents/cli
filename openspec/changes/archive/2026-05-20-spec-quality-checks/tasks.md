# Tasks: Spec Quality Checks

## 1. Shared helper

- [x] 1.1 Add `find_spec_files(path)` to `src/iec_cli/checkers/_shared.py` — scans `openspec/specs/**/*.md` and active change specs, excluding `archive/`

## 2. spec-ac-ids — implementation and proof

- [x] 2.1 Create `src/iec_cli/checkers/spec_ac_ids.py` — `SpecAcIds` class, uses `find_spec_files`, checks every `Scenario:` heading for `[PREFIX-NNN]` AC ID, registered via `@registry.register`
- [x] 2.2 Positive tests: no spec files returns PASS [ACID-001], all headings have IDs returns PASS [ACID-002]
- [x] 2.3 Negative tests: heading missing AC ID returns FAIL with heading in message [ACID-003], multiple scenarios one missing reports all violations [ACID-004]
- [x] 2.4 Registration test [ACID-005]

## 3. spec-test-category — implementation and proof

- [x] 3.1 Create `src/iec_cli/checkers/spec_test_category.py` — `SpecTestCategory` class, splits content on scenario headings, checks each body for `**Test:**`, registered via `@registry.register`
- [x] 3.2 Positive tests: no spec files returns PASS [STCT-001], all scenarios have **Test:** returns PASS [STCT-002]
- [x] 3.3 Negative tests: scenario missing **Test:** returns FAIL [STCT-003], multiple scenarios one missing reports all violations [STCT-004]
- [x] 3.4 Registration test [STCT-005]

## 4. Wiring

- [x] 4.1 Update `src/iec_cli/checkers/__init__.py` to import `spec_ac_ids`, `spec_test_category`
- [x] 4.2 Update integration test to register and assert new checkers appear in output

## 5. Verify

- [x] 5.1 Run `uv run ruff check` — no lint errors
- [x] 5.2 Run `uv run ruff format --check` — no formatting issues
- [x] 5.3 Run `uv run pytest -v` — all 10 AC IDs proven (ACID-001..005, STCT-001..005)
