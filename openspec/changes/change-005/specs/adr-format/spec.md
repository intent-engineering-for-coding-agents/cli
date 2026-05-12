# adr-format Specification

## ADDED Requirements

### Requirement: MADR filename convention

The system SHALL provide an `adr-format` checker that walks `docs/decisions/` for `*.md` files, skipping `README.md` and `INDEX.md`. For each remaining file the checker SHALL verify the filename matches `^\d{4}-[a-z0-9-]+\.md$`. Files that do not match SHALL be reported as violations.

#### Scenario: All ADR filenames are valid [ADRF-001]

**Test:** Unit

- **WHEN** all `.md` files in `docs/decisions/` (excluding README.md and INDEX.md) match `NNNN-kebab-case.md`
- **THEN** the result is `PASS`

#### Scenario: ADR filename missing 4-digit prefix [ADRF-002]

**Test:** Unit

- **WHEN** `docs/decisions/my-decision.md` exists (no numeric prefix)
- **THEN** the result is `FAIL` with a message mentioning `my-decision.md`

### Requirement: MADR title heading

The checker SHALL verify each ADR has a `#` title heading as its first non-empty line. If the heading uses the numbered format `# ADR-NNNN: <Title>`, the NNNN prefix SHALL match the filename prefix. A plain title without the `# ADR-NNNN:` prefix is also valid (used in YAML front matter style ADRs).

#### Scenario: ADR has no title heading [ADRF-003]

**Test:** Unit

- **WHEN** `docs/decisions/0001-my-decision.md` has no `#` heading as its first non-empty line
- **THEN** the result is `FAIL` with a message mentioning the missing heading

#### Scenario: ADR numbered title mismatches filename prefix [ADRF-004]

**Test:** Unit

- **WHEN** `docs/decisions/0001-my-decision.md` starts with `# ADR-0002: Wrong`
- **THEN** the result is `FAIL` with a message mentioning the number mismatch

#### Scenario: ADR has plain title heading (YAML style) [ADRF-012]

**Test:** Unit

- **WHEN** `docs/decisions/0001-my-decision.md` starts with `# My Decision` (no `# ADR-NNNN:` prefix)
- **THEN** the title check passes for that file

### Requirement: MADR required sections

The checker SHALL verify each ADR contains both `## Context and Problem Statement` and `## Decision Outcome` sections.

#### Scenario: ADR missing Context and Problem Statement section [ADRF-005]

**Test:** Unit

- **WHEN** `docs/decisions/0001-my-decision.md` lacks `## Context and Problem Statement`
- **THEN** the result is `FAIL` with a message mentioning the missing section

#### Scenario: ADR missing Decision Outcome section [ADRF-006]

**Test:** Unit

- **WHEN** `docs/decisions/0001-my-decision.md` lacks `## Decision Outcome`
- **THEN** the result is `FAIL` with a message mentioning the missing section

### Requirement: MADR status field

The checker SHALL verify each ADR declares a status in one of two formats:
- Bullet style: a `* Status: <value>` line in the document body
- YAML style: a `status: <value>` entry in YAML front matter (delimited by `---`)

The status value SHALL start with one of: `accepted`, `deprecated`, `superseded`, `proposed`. The `superseded` base word MAY be followed by a reference (e.g. `superseded by [ADR-0005](0005-example.md)`). An ADR with no status in either format, or whose status does not start with a recognised base word, SHALL be a violation.

#### Scenario: Bullet-style ADR has valid status [ADRF-007]

**Test:** Unit

- **WHEN** `docs/decisions/0001-my-decision.md` contains `* Status: accepted` (bullet style, no front matter)
- **THEN** that file passes the status check

#### Scenario: ADR has no status in either format [ADRF-008]

**Test:** Unit

- **WHEN** `docs/decisions/0001-my-decision.md` has neither a `* Status:` bullet nor a `status:` YAML field
- **THEN** the result is `FAIL` with a message mentioning the missing status

#### Scenario: Bullet-style ADR has unrecognised status value [ADRF-009]

**Test:** Unit

- **WHEN** `docs/decisions/0001-my-decision.md` contains `* Status: draft`
- **THEN** the result is `FAIL` with a message mentioning the invalid status value

#### Scenario: YAML front matter ADR has valid status [ADRF-013]

**Test:** Unit

- **WHEN** `docs/decisions/0001-my-decision.md` has `status: accepted` in YAML front matter
- **THEN** that file passes the status check

#### Scenario: YAML front matter ADR has unrecognised status value [ADRF-014]

**Test:** Unit

- **WHEN** `docs/decisions/0001-my-decision.md` has `status: draft` in YAML front matter
- **THEN** the result is `FAIL` with a message mentioning the invalid status value

#### Scenario: ADR has superseded status with reference [ADRF-015]

**Test:** Unit

- **WHEN** `docs/decisions/0001-my-decision.md` contains `* Status: superseded by [ADR-0003](0003-title.md)`
- **THEN** that file passes the status check (value starts with `superseded`)

### Requirement: Missing or empty decisions directory

When `docs/decisions/` does not exist or contains no `NNNN-*.md` files, the checker SHALL return `PASS` (no ADRs to validate).

#### Scenario: docs/decisions/ absent or empty [ADRF-010]

**Test:** Unit

- **WHEN** `docs/decisions/` does not exist, or exists but contains no `NNNN-*.md` files
- **THEN** the result is `PASS`

### Requirement: Checker registration

The checker SHALL register itself via `@registry.register` with `id` `"adr-format"`.

#### Scenario: Checker is registered [ADRF-011]

**Test:** Unit

- **WHEN** the checkers package is imported
- **THEN** `"adr-format"` appears in `registry.list_all()`
