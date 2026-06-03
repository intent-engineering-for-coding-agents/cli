# agents-hub-structure Specification

## Purpose

Validates that the `.agents/` agent instruction hub exists and contains both `instructions/` and `skills/` subdirectories. Without this structure, agents cannot load context files or invoke skills.

## Requirements

### Requirement: Hub directory structure

The checker SHALL verify that `.agents/`, `.agents/instructions/`, and `.agents/skills/` all exist as directories. Any missing item is a violation.

#### Scenario: .agents/ has instructions/ and skills/ [AHUB-001]

Test-type: unit

- **WHEN** `.agents/`, `.agents/instructions/`, and `.agents/skills/` all exist
- **THEN** the result is `PASS`

#### Scenario: .agents/ directory not found [AHUB-002]

Test-type: unit

- **WHEN** `.agents/` does not exist
- **THEN** the result is `FAIL` with ".agents/" in the message

#### Scenario: instructions/ subdirectory missing [AHUB-003]

Test-type: unit

- **WHEN** `.agents/` exists but `.agents/instructions/` does not
- **THEN** the result is `FAIL` with "instructions/" in the message

#### Scenario: skills/ subdirectory missing [AHUB-004]

Test-type: unit

- **WHEN** `.agents/` exists but `.agents/skills/` does not
- **THEN** the result is `FAIL` with "skills/" in the message

#### Scenario: Both subdirectories missing [AHUB-005]

Test-type: unit

- **WHEN** `.agents/` exists but neither `instructions/` nor `skills/` exist
- **THEN** the result is `FAIL` with both "instructions/" and "skills/" in the message

### Requirement: Checker registration

#### Scenario: Checker is registered [AHUB-006]

Test-type: unit

- **WHEN** the checkers package is imported
- **THEN** `"agents-hub-structure"` appears in `registry.list_all()`
