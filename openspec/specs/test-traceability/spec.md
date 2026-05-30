# test-traceability Specification

## Purpose

Cross-reference AC IDs found in spec scenario headings against machine-readable
test markers in test files. Ensures every non-Manual acceptance criterion has at
least one test proving it, and every test marker references a real AC ID.

---

## Requirements

### Requirement: Spec AC ID collection

The checker SHALL collect all `[PREFIX-NNN]` AC IDs from `Scenario:` headings
in `openspec/specs/**/*.md` and active change specs (excluding `archive/`), using
the same discovery logic as `spec-ac-ids`. Scenarios whose immediately following
body contains `Test-type: Manual` SHALL be excluded from coverage enforcement.

#### Scenario: No spec files found [TRTC-001]

Test-type: Unit

- **WHEN** `openspec/` does not exist or contains no spec `.md` files
- **THEN** the result is `PASS`

#### Scenario: All non-Manual AC IDs have test markers [TRTC-002]

Test-type: Unit

- **WHEN** every non-Manual spec scenario AC ID has at least one matching test marker
- **THEN** the result is `PASS`

#### Scenario: Non-Manual AC ID missing a test marker [TRTC-003]

Test-type: Unit

- **WHEN** a spec scenario AC ID has `Test-type:` other than `Manual` and no test
  file contains a matching marker
- **THEN** the result is `FAIL` with the missing AC ID in the message

#### Scenario: Multiple uncovered AC IDs reported together [TRTC-004]

Test-type: Unit

- **WHEN** several non-Manual spec AC IDs have no test markers
- **THEN** the result is `FAIL` and all missing IDs appear in the message

#### Scenario: Manual AC ID is exempt [TRTC-005]

Test-type: Unit

- **WHEN** a scenario has `Test-type: Manual` in its body
- **THEN** its AC ID is NOT required to have a test marker

---

### Requirement: Test marker discovery

The checker SHALL scan all `*.py` and `*.feature` files recursively under a
`tests/` directory at the repo root. Each file is searched for AC ID references
using the patterns below. The directory path MAY be overridden by the
`ASE_TESTS_DIR` environment variable.

Supported marker formats:

| Framework | Pattern |
|---|---|
| pytest | `@pytest.mark.ac("PREFIX-NNN")` |
| JUnit | `@Tag("PREFIX-NNN")` |
| Cucumber | `@AC:PREFIX-NNN` |
| Go / fallback | `// AC: PREFIX-NNN` |

#### Scenario: pytest mark.ac() marker recognised [TRTC-006]

Test-type: Unit

- **WHEN** a `.py` file contains `@pytest.mark.ac("PREFIX-NNN")`
- **THEN** `PREFIX-NNN` is counted as a covered AC ID

#### Scenario: JUnit @Tag marker recognised [TRTC-007]

Test-type: Unit

- **WHEN** a test file contains `@Tag("PREFIX-NNN")`
- **THEN** `PREFIX-NNN` is counted as a covered AC ID

#### Scenario: Cucumber @AC: marker recognised [TRTC-008]

Test-type: Unit

- **WHEN** a `.feature` file contains `@AC:PREFIX-NNN`
- **THEN** `PREFIX-NNN` is counted as a covered AC ID

#### Scenario: Inline comment marker recognised [TRTC-009]

Test-type: Unit

- **WHEN** a test file contains `// AC: PREFIX-NNN`
- **THEN** `PREFIX-NNN` is counted as a covered AC ID

---

### Requirement: Orphaned marker detection

A test marker that references an AC ID not present in any active spec SHALL
produce a `WARN` result rather than a `PASS`. This catches stale references
left after a spec scenario is removed.

#### Scenario: Orphaned test marker produces a warning [TRTC-010]

Test-type: Unit

- **WHEN** a test marker references `PREFIX-NNN` and no spec scenario carries
  that AC ID
- **THEN** the result is `WARN` with the orphaned AC ID in the message

---

### Requirement: Checker registration

The checker SHALL register itself via `@registry.register` with id
`"test-traceability"`.

#### Scenario: Checker is registered [TRTC-011]

Test-type: Unit

- **WHEN** the checkers package is imported
- **THEN** `"test-traceability"` appears in `registry.list_all()`
