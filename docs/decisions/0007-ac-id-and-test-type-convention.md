---
status: accepted
date: 2026-06-04
decision-makers: Intent Engineering for Coding Agents Contributors
---

# ADR-0007: AC ID and Test-Type Convention for iec-cli Specs

## Context and Problem Statement

iec-cli uses OpenSpec for spec-driven development. OpenSpec defines no standard for
acceptance criterion (AC) identifiers or test-type classification. Without a fixed
convention, IDs drift across specs (mixed formats, reused numbers, no clear prefix
ownership), and test traceability is unenforceable by machine.

The `test-traceability` checker (Change 009) requires a stable, machine-readable AC ID
format. The `spec-test-category` checker (Change 006) requires a `Test-type:` field in
every scenario body. This ADR captures the format decisions so they are grounded, not
implicit.

## Considered Options

* `[PREFIX-NNN]` in scenario headings + `Test-type:` field in scenario body
* YAML front matter per scenario (heavier, less readable)
* Free-text tags (no machine-readable convention)

## Decision Outcome

Chosen option: `[PREFIX-NNN]` AC IDs and `Test-type:` field, because the format is
lightweight (three extra tokens per scenario), grep-able, and directly supported by the
existing `spec-ac-ids`, `spec-test-category`, and `test-traceability` checkers.

### AC ID Format

```
[PREFIX-NNN]
```

- `PREFIX`: 2-6 uppercase letters or digits identifying the capability (see registry
  in `tests/ac-registry.md`)
- `NNN`: monotone integer, zero-padded to 3 digits, never reused after deletion
- IDs appear at the end of a `#### Scenario:` heading line

### Test-Type Field

```
Test-type: <value>
```

Appears as the first non-blank line in the scenario body. Recognised values:

| Value | Meaning |
|---|---|
| `Unit` | Pure-function test, no I/O, no CLI invocation |
| `Integration` | CLI invocation via `typer.testing.CliRunner` + real filesystem |
| `Manual` | Cannot be automated; excluded from traceability enforcement |
| `Sanity` | Environment or toolchain readiness test |

### Pytest Marker Convention

Test functions proving an AC carry `@pytest.mark.ac("PREFIX-NNN")`. A test proving
multiple ACs carries multiple decorators. Test-type maps to `@pytest.mark.unit`,
`@pytest.mark.integration`, or `@pytest.mark.sanity`.

### Consequences

* Good, because the `test-traceability` and `spec-test-category` checkers can enforce
  this convention deterministically
* Good, because AC IDs are monotone — no renumbering, clear audit trail
* Good, because the `Manual` exemption keeps human-verified scenarios out of the
  automated traceability scan
* Neutral, because every new spec requires an upfront prefix allocation in
  `tests/ac-registry.md`
