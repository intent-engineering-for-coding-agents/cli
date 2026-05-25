# spec-ac-ids Specification

## Purpose

Validates that every `#### Scenario:` heading in every spec file under `openspec/` contains a `[PREFIX-NNN]` AC ID. AC IDs are required for test traceability and cross-referencing.

## Requirements

### Requirement: Spec file discovery

The checker SHALL scan `openspec/specs/**/*.md` (canonical specs) and `openspec/changes/*/specs/**/*.md` (active change specs), excluding `openspec/changes/archive/`.

#### Scenario: No spec files found [ACID-001]

Test-type: unit

- **WHEN** `openspec/` does not exist or contains no spec `.md` files
- **THEN** the result is `PASS`

### Requirement: AC ID presence in scenario headings

The checker SHALL identify every heading matching `^#{3,6}\s+Scenario:\s+.+$`. Each such heading MUST contain a `[PREFIX-NNN]` pattern where PREFIX is 2+ uppercase letters or digits.

#### Scenario: All scenario headings have AC IDs [ACID-002]

Test-type: unit

- **WHEN** every `Scenario:` heading in every spec file contains a `[PREFIX-NNN]` AC ID
- **THEN** the result is `PASS`

#### Scenario: A scenario heading is missing an AC ID [ACID-003]

Test-type: unit

- **WHEN** a `Scenario:` heading contains no `[PREFIX-NNN]` pattern
- **THEN** the result is `FAIL` with the heading text in the message

#### Scenario: Multiple scenarios, one missing AC ID [ACID-004]

Test-type: unit

- **WHEN** multiple `Scenario:` headings exist and one lacks a `[PREFIX-NNN]` pattern
- **THEN** the result is `FAIL` with all violated headings reported

### Requirement: Checker registration

The checker SHALL register itself via `@registry.register` with `id` `"spec-ac-ids"`.

#### Scenario: Checker is registered [ACID-005]

Test-type: unit

- **WHEN** the checkers package is imported
- **THEN** `"spec-ac-ids"` appears in `registry.list_all()`
