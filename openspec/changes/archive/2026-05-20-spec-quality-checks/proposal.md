# Proposal: Spec Quality Checks

## Why

Specs without AC IDs cannot be cross-referenced by `test-traceability`. Specs without `**Test:**` fields leave test layer undefined. Both are structural gaps that compound — once specs accumulate without these fields, the AC ID and coverage checks planned for Phase G have nothing to anchor to.

## What Changes

- **`spec-ac-ids` checker**: Walks `openspec/specs/` and active `openspec/changes/*/specs/` for `*.md` files. For each `#### Scenario:` heading, verifies a `[PREFIX-NNN]` AC ID is present. Returns FAIL listing all violations.
- **`spec-test-category` checker**: Same file discovery. For each scenario section, verifies a `**Test:**` field appears before the next heading. Returns FAIL listing all violations.
- Each checker is a class conforming to the `Checker` protocol, registered via `@registry.register`.
- Shared `find_spec_files()` helper added to `_shared.py`.

## Capabilities

### New Capabilities

- `spec-ac-ids`: Checks that every `#### Scenario:` heading in every spec file contains a `[PREFIX-NNN]` AC ID. FAIL if any heading is missing one.
- `spec-test-category`: Checks that every scenario section in every spec file contains a `**Test:**` field. FAIL if any section is missing one.

### Modified Capabilities

- `_shared.py`: Adds `find_spec_files(path)` — locates canonical and active change spec files.

## Impact

- **New modules**: `src/iec_cli/checkers/spec_ac_ids.py`, `src/iec_cli/checkers/spec_test_category.py`
- **Updated**: `src/iec_cli/checkers/_shared.py`, `src/iec_cli/checkers/__init__.py`
- **Tests**: 10 unit tests (ACID-001..005, STCT-001..005)
- **No new dependencies**
