# docs-index-stale Specification

## Purpose
TBD - created by archiving change architecture-file-checks. Update Purpose after archive.
## Requirements
### Requirement: INDEX.md cross-reference check (per-directory)

The system SHALL provide a `docs-index-stale` checker that:
- Walks `docs/` recursively, finds every `INDEX.md`
- For each INDEX.md, parses Markdown links `[text](path)` treating paths as relative to that INDEX.md's directory
- Compares referenced paths against actual files in that same directory
- Reports referenced files that do not exist (broken links)
- Reports files in that directory (excluding `.gitkeep`) not referenced in INDEX.md (orphans)

#### Scenario: All INDEX files match filesystem [DINS-001]

**Test:** Unit

- **WHEN** every INDEX.md under `docs/` accurately lists the files in its directory
- **THEN** the result is `PASS`

#### Scenario: Broken link in an INDEX.md [DINS-002]

**Test:** Unit

- **WHEN** `docs/INDEX.md` references `missing-file.md` that does not exist in `docs/`
- **THEN** the result is `WARN` with message listing the broken link

#### Scenario: Orphan file in a directory [DINS-003]

**Test:** Unit

- **WHEN** `docs/decisions/unlisted.md` exists but is not referenced in `docs/decisions/INDEX.md`
- **THEN** the result is `WARN` with message listing the orphan file

#### Scenario: Both broken and orphan across multiple INDEX files [DINS-004]

**Test:** Unit

- **WHEN** one INDEX.md has a broken link and another has an orphan file
- **THEN** the result is `WARN` listing both issues

#### Scenario: .gitkeep files excluded from orphans [DINS-005]

**Test:** Unit

- **WHEN** `docs/architecture/.gitkeep` exists but is not in INDEX.md
- **THEN** the `.gitkeep` file is NOT reported as an orphan

#### Scenario: docs/ directory missing entirely [DINS-006]

**Test:** Unit

- **WHEN** `docs/` directory does not exist at all
- **THEN** the result is `FAIL` with appropriate message

### Requirement: checker registration

The checker SHALL register itself via `@registry.register` with `id` `"docs-index-stale"`.

#### Scenario: Checker is registered [DINS-007]

**Test:** Unit

- **WHEN** the checkers package is imported
- **THEN** `"docs-index-stale"` appears in `registry.list_all()`

