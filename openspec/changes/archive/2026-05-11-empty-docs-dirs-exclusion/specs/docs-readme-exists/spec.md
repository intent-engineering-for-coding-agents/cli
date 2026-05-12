# Docs README Exists — empty-dir exclusion

Adds an exemption: effectively-empty subdirectories of `docs/` do not require `README.md`.

## ADDED Requirements

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
