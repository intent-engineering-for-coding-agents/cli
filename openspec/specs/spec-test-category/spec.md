# spec-test-category Specification

## Purpose

Validates that every `#### Scenario:` section in every spec file under `openspec/` contains a `Test-type:` field. The test layer declaration is required for coverage analysis and CI planning.

## Requirements

### Requirement: Spec file discovery

The checker uses the same discovery as `spec-ac-ids`: canonical specs plus active change specs, excluding archived changes.

#### Scenario: No spec files found [STCT-001]

Test-type: unit

- **WHEN** `openspec/` does not exist or contains no spec `.md` files
- **THEN** the result is `PASS`

### Requirement: Test-type: field presence per scenario

The checker SHALL split spec content on `Scenario:` headings and check each resulting section for a `Test-type:` field before the next heading.

#### Scenario: All scenario sections have Test-type: field [STCT-002]

Test-type: unit

- **WHEN** every scenario section in every spec file contains a `Test-type:` field
- **THEN** the result is `PASS`

#### Scenario: A scenario section is missing Test-type: field [STCT-003]

Test-type: unit

- **WHEN** a scenario section contains no `Test-type:` field
- **THEN** the result is `FAIL` with the scenario heading in the message

#### Scenario: Multiple scenarios, one missing Test-type: field [STCT-004]

Test-type: unit

- **WHEN** multiple scenario sections exist and one lacks a `Test-type:` field
- **THEN** the result is `FAIL` with all violated scenario headings reported

### Requirement: Checker registration

The checker SHALL register itself via `@registry.register` with `id` `"spec-test-category"`.

#### Scenario: Checker is registered [STCT-005]

Test-type: unit

- **WHEN** the checkers package is imported
- **THEN** `"spec-test-category"` appears in `registry.list_all()`
