## MODIFIED Requirements

### Requirement: AGENTS.md line count check

The system SHALL provide an `agents-size` checker that counts lines in `AGENTS.md` and compares against a configurable limit. The limit SHALL default to 50 lines and SHALL be overridable via the `ASE_AGENTS_MAX_LINES` environment variable. A leading YAML front matter block, from a first line of `---` through the next line that is exactly `---`, SHALL NOT count toward the total. A file whose first line is `---` with no closing `---` SHALL be counted in full.

#### Scenario: AGENTS.md under limit [AGSZ-001]

Test-type: unit

- **WHEN** `AGENTS.md` has 30 lines and the limit is 50
- **THEN** the result is `PASS` with message "AGENTS.md is 30 lines (limit: 50)"

#### Scenario: AGENTS.md exceeds limit [AGSZ-002]

Test-type: unit

- **WHEN** `AGENTS.md` has 72 lines and the limit is 50
- **THEN** the result is `FAIL` with message "AGENTS.md has 72 lines (limit: 50)"

#### Scenario: custom limit via environment variable [AGSZ-003]

Test-type: unit

- **WHEN** `ASE_AGENTS_MAX_LINES` is set to `100` and `AGENTS.md` has 80 lines
- **THEN** the result is `PASS`

#### Scenario: AGENTS.md missing [AGSZ-004]

Test-type: unit

- **WHEN** `AGENTS.md` does not exist at the repo root
- **THEN** the result is `FAIL` with message indicating file not found

#### Scenario: invalid env var value [AGSZ-005]

Test-type: unit

- **WHEN** `ASE_AGENTS_MAX_LINES` is set to a non-integer value
- **THEN** the checker uses the default limit of 50

#### Scenario: front matter does not count toward the limit [AGSZ-007]

Test-type: unit

- **WHEN** `AGENTS.md` has a 4-line front matter block followed by 48 lines of content, 52 lines in total, and the limit is 50
- **THEN** the result is `PASS` with message "AGENTS.md is 48 lines excluding 4 front matter lines (limit: 50)"

#### Scenario: content over the limit still fails with front matter present [AGSZ-008]

Test-type: unit

- **WHEN** `AGENTS.md` has a 4-line front matter block followed by 51 lines of content and the limit is 50
- **THEN** the result is `FAIL` with message "AGENTS.md has 51 lines excluding 4 front matter lines (limit: 50)"

#### Scenario: unterminated front matter is counted in full [AGSZ-009]

Test-type: unit

- **WHEN** the first line of `AGENTS.md` is `---`, no later line is exactly `---`, and the file has 52 lines
- **THEN** the result is `FAIL` with message "AGENTS.md has 52 lines (limit: 50)"

#### Scenario: a horizontal rule later in the file is not front matter [AGSZ-010]

Test-type: unit

- **WHEN** `AGENTS.md` starts with a heading, contains a `---` line at line 20, and has 52 lines
- **THEN** the result is `FAIL` with message "AGENTS.md has 52 lines (limit: 50)"
