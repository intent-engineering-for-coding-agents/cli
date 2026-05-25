# file-size Specification

## Purpose

Warns when any `.md` file in the repo exceeds a configurable line limit. Oversized documentation files are harder to navigate and harder for agents to hold in context.

## Requirements

### Requirement: File size limit

The checker SHALL walk all `.md` files recursively from the repo root. It SHALL skip directories named `.git`, `node_modules`, `.venv`, `venv`, `__pycache__`, and `.vitepress`. Files exceeding the limit SHALL be reported as WARN.

The default limit is 500 lines. Overridden by `ASE_FILE_MAX_LINES`. If invalid, fall back to default.

#### Scenario: All .md files within limit [FLSZ-001]

Test-type: unit

- **WHEN** all `.md` files have 500 or fewer lines
- **THEN** the result is `PASS`

#### Scenario: A .md file exceeds the limit [FLSZ-002]

Test-type: unit

- **WHEN** a `.md` file has more than 500 lines
- **THEN** the result is `WARN` with the filename and line count in the message

#### Scenario: Env var overrides limit [FLSZ-003]

Test-type: unit

- **WHEN** `ASE_FILE_MAX_LINES=50` and a `.md` file has 80 lines
- **THEN** the result is `WARN`

### Requirement: No .md files

#### Scenario: No .md files found [FLSZ-004]

Test-type: unit

- **WHEN** the repo contains no `.md` files outside skip directories
- **THEN** the result is `PASS`

### Requirement: Skip common non-project directories

#### Scenario: .md files inside node_modules/ are not counted [FLSZ-005]

Test-type: unit

- **WHEN** `node_modules/some-pkg/README.md` has 600 lines and no other `.md` files exceed the limit
- **THEN** the result is `PASS`

### Requirement: Invalid env var fallback

#### Scenario: Invalid ASE_FILE_MAX_LINES falls back to default [FLSZ-006]

Test-type: unit

- **WHEN** `ASE_FILE_MAX_LINES=not-a-number` and a `.md` file has 100 lines
- **THEN** the result is `PASS` (default 500 applies)

### Requirement: Checker registration

#### Scenario: Checker is registered [FLSZ-007]

Test-type: unit

- **WHEN** the checkers package is imported
- **THEN** `"file-size"` appears in `registry.list_all()`
