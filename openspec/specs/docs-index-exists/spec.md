# docs-index-exists Specification

## Purpose
TBD - created by archiving change architecture-file-checks. Update Purpose after archive.
## Requirements
### Requirement: Recursive INDEX.md presence check

The system SHALL provide a `docs-index-exists` checker that walks the `docs/` directory tree recursively. Every subdirectory under `docs/` (including `docs/` itself) SHOULD contain an `INDEX.md`. The checker SHALL return PASS when all directories have INDEX.md, and WARN listing any missing directories.

#### Scenario: All directories have INDEX.md [DINE-001]

Test-type: unit

- **WHEN** `docs/` contains `INDEX.md` and all subdirectories contain `INDEX.md`
- **THEN** the result is `PASS`

#### Scenario: Missing INDEX.md in a subdirectory [DINE-002]

Test-type: unit

- **WHEN** `docs/decisions/` exists but has no `INDEX.md`
- **THEN** the result is `WARN` with message listing `docs/decisions/` as missing

#### Scenario: Multiple directories missing INDEX.md [DINE-003]

Test-type: unit

- **WHEN** multiple subdirectories under `docs/` lack `INDEX.md`
- **THEN** the result is `WARN` listing all missing directories

#### Scenario: docs/ directory missing entirely [DINE-004]

Test-type: unit

- **WHEN** `docs/` directory does not exist at all
- **THEN** the result is `FAIL` with appropriate message

### Requirement: checker registration

The checker SHALL register itself via `@registry.register` with `id` `"docs-index-exists"`.

#### Scenario: Checker is registered [DINE-005]

Test-type: unit

- **WHEN** the checkers package is imported
- **THEN** `"docs-index-exists"` appears in `registry.list_all()`

### Requirement: Effectively-empty directories are exempt

The checker SHALL skip any subdirectory of `docs/` that is *effectively empty* — i.e. its subtree contains no regular files except entries whose name begins with `.` (such as `.gitkeep`, `.hidden`, `.DS_Store`). Such placeholder directories SHALL NOT be reported as missing `INDEX.md`.

#### Scenario: Subdirectory with only .gitkeep is skipped [DINE-006]

Test-type: unit

- **WHEN** `docs/design/` contains only `.gitkeep`
- **THEN** the result is `PASS` and `docs/design` is not listed as missing

#### Scenario: Subdirectory with only dotfiles is skipped [DINE-006]

Test-type: unit

- **WHEN** `docs/design/` contains only `.gitkeep`, `.hidden`, `.DS_Store`
- **THEN** the result is `PASS`

#### Scenario: Nested empty subdirectory is skipped [DINE-006]

Test-type: unit

- **WHEN** `docs/design/wip/` contains only `.gitkeep` (and no other files anywhere below `docs/design/`)
- **THEN** the result is `PASS`

#### Scenario: Substantive content alongside .gitkeep still requires INDEX [DINE-006]

Test-type: unit

- **WHEN** `docs/design/` contains `.gitkeep` and a regular file (e.g. `draft.md`)
- **THEN** the result is `WARN` and `docs/design` is listed as missing

