# Docs README Exists

Recursively checks that every subdirectory under `docs/` contains a `README.md`.

## ADDED Requirements

### Requirement: Recursive README.md presence check

The system SHALL provide a `docs-readme-exists` checker that walks the `docs/` directory tree recursively. Every subdirectory under `docs/` (including `docs/` itself) SHALL contain a `README.md`. The checker SHALL return PASS when all directories have README.md, and FAIL listing any missing directories.

#### Scenario: All directories have README.md [DRME-001]

**Test:** Unit

- **WHEN** `docs/` contains `README.md` and all subdirectories contain `README.md`
- **THEN** the result is `PASS`

#### Scenario: Missing README.md in a subdirectory [DRME-002]

**Test:** Unit

- **WHEN** `docs/architecture/` exists but has no `README.md`
- **THEN** the result is `FAIL` with message listing `docs/architecture/` as missing

#### Scenario: Multiple directories missing README.md [DRME-003]

**Test:** Unit

- **WHEN** multiple subdirectories under `docs/` lack `README.md`
- **THEN** the result is `FAIL` listing all missing directories

#### Scenario: docs/ directory missing entirely [DRME-004]

**Test:** Unit

- **WHEN** `docs/` directory does not exist at all
- **THEN** the result is `FAIL` with appropriate message

### Requirement: checker registration

The checker SHALL register itself via `@registry.register` with `id` `"docs-readme-exists"`.

#### Scenario: Checker is registered [DRME-005]

**Test:** Unit

- **WHEN** the checkers package is imported
- **THEN** `"docs-readme-exists"` appears in `registry.list_all()`
