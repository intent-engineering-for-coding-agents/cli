# Agents Size

Checks that `AGENTS.md` is under a configurable line limit.

## ADDED Requirements

### Requirement: AGENTS.md line count check

The system SHALL provide an `agents-size` checker that counts lines in `AGENTS.md` and compares against a configurable limit. The limit SHALL default to 50 lines and SHALL be overridable via the `ASE_AGENTS_MAX_LINES` environment variable.

#### Scenario: AGENTS.md under limit [AGSZ-001]

**Test:** Unit

- **WHEN** `AGENTS.md` has 30 lines and the limit is 50
- **THEN** the result is `PASS` with message "AGENTS.md is 30 lines (limit: 50)"

#### Scenario: AGENTS.md exceeds limit [AGSZ-002]

**Test:** Unit

- **WHEN** `AGENTS.md` has 72 lines and the limit is 50
- **THEN** the result is `FAIL` with message "AGENTS.md has 72 lines (limit: 50)"

#### Scenario: custom limit via environment variable [AGSZ-003]

**Test:** Unit

- **WHEN** `ASE_AGENTS_MAX_LINES` is set to `100` and `AGENTS.md` has 80 lines
- **THEN** the result is `PASS`

#### Scenario: AGENTS.md missing [AGSZ-004]

**Test:** Unit

- **WHEN** `AGENTS.md` does not exist at the repo root
- **THEN** the result is `FAIL` with message indicating file not found

#### Scenario: invalid env var value [AGSZ-005]

**Test:** Unit

- **WHEN** `ASE_AGENTS_MAX_LINES` is set to a non-integer value
- **THEN** the checker uses the default limit of 50

### Requirement: checker registration

The checker SHALL register itself via `@registry.register` with `id` `"agents-size"` and a description summarizing the line limit check.

#### Scenario: Checker is registered [AGSZ-006]

**Test:** Unit

- **WHEN** the checkers package is imported
- **THEN** `"agents-size"` appears in `registry.list_all()`
