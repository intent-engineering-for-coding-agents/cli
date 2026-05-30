# test-coverage Specification

## Purpose

Enforce the positive + negative proof requirement from the ASE testing convention.
Every non-Manual acceptance criterion SHALL be covered by at least two test markers
(the minimum proxy for positive and negative equivalence classes). A single test
marker is necessary but insufficient.

---

## Requirements

### Requirement: Minimum marker count per AC

For each non-Manual AC ID collected from spec files, the checker SHALL count how
many distinct test markers (across all test files) reference that ID. If fewer
than 2 markers are found for an otherwise covered AC, the checker SHALL produce
a `WARN` result. ACs with 0 markers are the domain of `test-traceability` (FAIL),
not this checker.

#### Scenario: No spec files found [TCOV-001]

Test-type: Unit

- **WHEN** `openspec/` does not exist or contains no spec `.md` files
- **THEN** the result is `PASS`

#### Scenario: All non-Manual ACs have 2 or more markers [TCOV-002]

Test-type: Unit

- **WHEN** every non-Manual AC ID has at least 2 test markers referencing it
- **THEN** the result is `PASS`

#### Scenario: Non-Manual AC with exactly 1 marker [TCOV-003]

Test-type: Unit

- **WHEN** a non-Manual AC ID has exactly 1 test marker
- **THEN** the result is `WARN` with the under-covered AC ID in the message

#### Scenario: Multiple under-covered ACs reported together [TCOV-004]

Test-type: Unit

- **WHEN** several non-Manual ACs each have exactly 1 test marker
- **THEN** the result is `WARN` and all under-covered IDs appear in the message

#### Scenario: Manual AC ID is exempt [TCOV-005]

Test-type: Unit

- **WHEN** a scenario carries `Test-type: Manual` in its body
- **THEN** its AC ID is NOT subject to the minimum marker count

#### Scenario: AC with 0 markers is not double-reported [TCOV-006]

Test-type: Unit

- **WHEN** a non-Manual AC has 0 test markers (uncovered)
- **THEN** this checker returns `PASS` (the uncovered case belongs to `test-traceability`)

---

### Requirement: Checker registration

The checker SHALL register itself via `@registry.register` with id
`"test-coverage"`.

#### Scenario: Checker is registered [TCOV-007]

Test-type: Unit

- **WHEN** the checkers package is imported
- **THEN** `"test-coverage"` appears in `registry.list_all()`
