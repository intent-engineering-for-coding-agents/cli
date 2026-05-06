# docs-index-exists Specification

## Purpose
TBD - created by archiving change architecture-file-checks. Update Purpose after archive.
## Requirements
### Requirement: Recursive INDEX.md presence check

The system SHALL provide a `docs-index-exists` checker that walks the `docs/` directory tree recursively. Every subdirectory under `docs/` (including `docs/` itself) SHOULD contain an `INDEX.md`. The checker SHALL return PASS when all directories have INDEX.md, and WARN listing any missing directories.

#### Scenario: All directories have INDEX.md [DINE-001]

**Test:** Unit

- **WHEN** `docs/` contains `INDEX.md` and all subdirectories contain `INDEX.md`
- **THEN** the result is `PASS`

#### Scenario: Missing INDEX.md in a subdirectory [DINE-002]

**Test:** Unit

- **WHEN** `docs/decisions/` exists but has no `INDEX.md`
- **THEN** the result is `WARN` with message listing `docs/decisions/` as missing

#### Scenario: Multiple directories missing INDEX.md [DINE-003]

**Test:** Unit

- **WHEN** multiple subdirectories under `docs/` lack `INDEX.md`
- **THEN** the result is `WARN` listing all missing directories

#### Scenario: docs/ directory missing entirely [DINE-004]

**Test:** Unit

- **WHEN** `docs/` directory does not exist at all
- **THEN** the result is `FAIL` with appropriate message

### Requirement: checker registration

The checker SHALL register itself via `@registry.register` with `id` `"docs-index-exists"`.

#### Scenario: Checker is registered [DINE-005]

**Test:** Unit

- **WHEN** the checkers package is imported
- **THEN** `"docs-index-exists"` appears in `registry.list_all()`

