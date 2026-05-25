# spec-size Specification

## Purpose

Warns when spec files exceed a configurable line limit. Oversized specs lose agent focus; this check flags them early so they can be split before they compound drift.

## Requirements

### Requirement: Spec size limit

The checker SHALL scan the same spec files as `spec-ac-ids`. For each file, it SHALL count lines using `splitlines()`. Files exceeding the limit SHALL be reported as WARN (not FAIL — size is advisory).

The default limit is 500 lines. The limit is overridden by the `ASE_SPEC_MAX_LINES` environment variable. If the variable is set but not a valid integer, the checker SHALL fall back to the default.

#### Scenario: Spec file within default limit [SPSZ-001]

Test-type: unit

- **WHEN** all spec files have 500 or fewer lines
- **THEN** the result is `PASS`

#### Scenario: Spec file exceeds default limit [SPSZ-002]

Test-type: unit

- **WHEN** a spec file has more than 500 lines
- **THEN** the result is `WARN` with the filename and line count in the message

#### Scenario: Env var overrides limit [SPSZ-003]

Test-type: unit

- **WHEN** `ASE_SPEC_MAX_LINES=50` is set and a spec file has 80 lines
- **THEN** the result is `WARN`

### Requirement: No spec files

When no spec files exist, the checker SHALL return PASS.

#### Scenario: No spec files found [SPSZ-004]

Test-type: unit

- **WHEN** `openspec/` does not exist or contains no spec files
- **THEN** the result is `PASS`

### Requirement: Invalid env var fallback

#### Scenario: Invalid ASE_SPEC_MAX_LINES falls back to default [SPSZ-005]

Test-type: unit

- **WHEN** `ASE_SPEC_MAX_LINES=not-a-number` is set and the spec file has 100 lines
- **THEN** the result is `PASS` (default 500 applies)

### Requirement: Checker registration

#### Scenario: Checker is registered [SPSZ-006]

Test-type: unit

- **WHEN** the checkers package is imported
- **THEN** `"spec-size"` appears in `registry.list_all()`
