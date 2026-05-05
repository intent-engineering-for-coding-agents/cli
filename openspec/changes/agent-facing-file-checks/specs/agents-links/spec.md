# Agents Links

Checks that every link in `AGENTS.md` has descriptive text — no bare URLs or naked paths.

## ADDED Requirements

### Requirement: AGENTS.md link description check

The system SHALL provide an `agents-links` checker that parses `AGENTS.md` for Markdown inline links `[text](url)` and reports any that lack trailing descriptive text on the same line. A bare link is a list item where the line ends immediately after the link without a description separator (space-dash-space or similar descriptive text).

#### Scenario: All links have descriptions [AGLN-001]

**Test:** Unit

- **WHEN** `AGENTS.md` contains `- [Build and CI](.agents/instructions/build-and-ci.md) — uv commands, lint, test`
- **THEN** the result is `PASS`

#### Scenario: Bare link found [AGLN-002]

**Test:** Unit

- **WHEN** `AGENTS.md` contains `- [Build and CI](.agents/instructions/build-and-ci.md)` with no trailing description
- **THEN** the result is `WARN` with message listing the bare link file path

#### Scenario: Multiple bare links [AGLN-003]

**Test:** Unit

- **WHEN** `AGENTS.md` has multiple list items with bare links
- **THEN** the result is `WARN` with message listing all bare link locations

#### Scenario: Non-list-item links are ignored [AGLN-004]

**Test:** Unit

- **WHEN** `AGENTS.md` has a bare link in a paragraph (not a list item) with no trailing description
- **THEN** that link is still flagged if it lacks descriptive text

#### Scenario: AGENTS.md missing [AGLN-005]

**Test:** Unit

- **WHEN** `AGENTS.md` does not exist at the repo root
- **THEN** the result is `FAIL` with message indicating file not found

### Requirement: checker registration

The checker SHALL register itself via `@registry.register` with `id` `"agents-links"` and a description summarizing the link quality check.

#### Scenario: Checker is registered [AGLN-006]

**Test:** Unit

- **WHEN** the checkers package is imported
- **THEN** `"agents-links"` appears in `registry.list_all()`
