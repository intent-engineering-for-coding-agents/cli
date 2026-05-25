# adr-index Specification

## Purpose

Validates that `docs/decisions/README.md` exists and lists every ADR file (`NNNN-*.md`) present in the `docs/decisions/` directory, ensuring the index stays complete.

## Requirements

### Requirement: ADR index existence check

The system SHALL provide an `adr-index` checker. When `docs/decisions/` is absent or contains no `NNNN-*.md` files, the result SHALL be `PASS` (no ADRs to index). When `NNNN-*.md` files are present and `docs/decisions/README.md` is missing, the result SHALL be `FAIL`.

#### Scenario: README.md exists and all ADRs are listed [ADRI-001]

Test-type: unit

- **WHEN** `docs/decisions/README.md` exists and contains a link to every `NNNN-*.md` file in the directory
- **THEN** the result is `PASS`

#### Scenario: docs/decisions/README.md missing when ADRs exist [ADRI-002]

Test-type: unit

- **WHEN** `docs/decisions/` contains `NNNN-*.md` files but no `README.md`
- **THEN** the result is `FAIL` with a message noting the missing index file

#### Scenario: docs/decisions/ absent or empty [ADRI-003]

Test-type: unit

- **WHEN** `docs/decisions/` does not exist, or exists but contains no `NNNN-*.md` files
- **THEN** the result is `PASS`

### Requirement: ADR completeness check

For each `NNNN-*.md` file found in `docs/decisions/`, the checker SHALL verify that `docs/decisions/README.md` contains at least one Markdown link referencing that filename. Files not linked in README.md SHALL be reported as unlisted ADRs.

#### Scenario: All ADRs linked in README.md [ADRI-004]

Test-type: unit

- **WHEN** every `NNNN-*.md` file in `docs/decisions/` has a corresponding Markdown link in README.md
- **THEN** the result is `PASS`

#### Scenario: One ADR not linked in README.md [ADRI-005]

Test-type: unit

- **WHEN** `docs/decisions/0007-new-decision.md` exists but is not referenced in README.md
- **THEN** the result is `FAIL` with a message mentioning `0007-new-decision.md`

#### Scenario: Multiple ADRs not listed [ADRI-006]

Test-type: unit

- **WHEN** two `NNNN-*.md` files are absent from README.md
- **THEN** the result is `FAIL` listing both filenames

### Requirement: Checker registration

The checker SHALL register itself via `@registry.register` with `id` `"adr-index"`.

#### Scenario: Checker is registered [ADRI-007]

Test-type: unit

- **WHEN** the checkers package is imported
- **THEN** `"adr-index"` appears in `registry.list_all()`
