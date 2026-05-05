# agents-exists Specification

## Purpose
TBD - created by archiving change agent-facing-file-checks. Update Purpose after archive.
## Requirements
### Requirement: AGENTS.md existence check

The system SHALL provide an `agents-exists` checker that verifies `AGENTS.md` exists at the repo root. The checker SHALL return `PASS` when found and `FAIL` when missing.

#### Scenario: AGENTS.md found [AGEX-001]

**Test:** Unit

- **WHEN** the checker runs against a repo where `AGENTS.md` exists at the root
- **THEN** the result is `PASS` with message "AGENTS.md found"

#### Scenario: AGENTS.md missing [AGEX-002]

**Test:** Unit

- **WHEN** the checker runs against a repo where `AGENTS.md` does not exist at the root
- **THEN** the result is `FAIL` with message "AGENTS.md not found"

### Requirement: checker registration

The checker SHALL register itself with the global `registry` via `@registry.register` decorator. The checker SHALL have an `id` of `"agents-exists"` and a `description` summarizing what it validates.

#### Scenario: Checker is registered [AGEX-003]

**Test:** Unit

- **WHEN** the checkers package is imported
- **THEN** `"agents-exists"` appears in `registry.list_all()`

