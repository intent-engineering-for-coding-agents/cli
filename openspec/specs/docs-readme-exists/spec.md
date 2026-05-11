# docs-readme-exists Specification

## Purpose
TBD - created by archiving change architecture-file-checks. Update Purpose after archive.
## Requirements
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

### Requirement: Effectively-empty directories are exempt

The checker SHALL skip any subdirectory of `docs/` that is *effectively empty* — i.e. its subtree contains no regular files except entries whose name begins with `.` (such as `.gitkeep`, `.hidden`, `.DS_Store`). Such placeholder directories SHALL NOT be reported as missing `README.md`.

#### Scenario: Subdirectory with only .gitkeep is skipped [DRME-006]

**Test:** Unit

- **WHEN** `docs/design/` contains only `.gitkeep`
- **THEN** the result is `PASS` and `docs/design` is not listed as missing

#### Scenario: Subdirectory with only dotfiles is skipped [DRME-006]

**Test:** Unit

- **WHEN** `docs/design/` contains only `.gitkeep`, `.hidden`, `.DS_Store`
- **THEN** the result is `PASS`

#### Scenario: Nested empty subdirectory is skipped [DRME-006]

**Test:** Unit

- **WHEN** `docs/design/wip/` contains only `.gitkeep` (and no other files anywhere below `docs/design/`)
- **THEN** the result is `PASS`

#### Scenario: Substantive content alongside .gitkeep still requires README [DRME-006]

**Test:** Unit

- **WHEN** `docs/design/` contains `.gitkeep` and a regular file (e.g. `draft.md`)
- **THEN** the result is `FAIL` and `docs/design` is listed as missing

