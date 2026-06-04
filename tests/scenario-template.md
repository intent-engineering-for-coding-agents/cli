# Scenario Template and Complexity-Tier Coverage Requirements

## Canonical Scenario Format

```markdown
#### Scenario: <brief description> [PREFIX-NNN]

Test-type: Unit | Integration | Manual | Sanity

- **WHEN** <precondition or action>
- **THEN** <expected result>
```

Rules:
- Heading level is `####` (four hashes), always under a `### Requirement:` section
- AC ID `[PREFIX-NNN]` appears at the end of the heading line, inside brackets
- `Test-type:` is the first non-blank line in the scenario body — exactly one value
- WHEN/THEN bullets use bold labels exactly as shown

---

## Complexity Tiers and Coverage Requirements

| Tier | Definition | Positive tests | Negative / edge tests |
|---|---|---|---|
| **Simple** | Single happy path, one obvious failure | 1 | 1 |
| **Medium** | 2-3 meaningful paths, one edge case | 2-3 | 2 |
| **Complex** | Many paths, config variants, error conditions | Several | Several |

"Positive test" = a test that exercises the happy path and asserts PASS or expected
success output.

"Negative / edge test" = a test that exercises a failure or boundary condition and
asserts FAIL, WARN, or an exception.

### Classifying a checker as Simple / Medium / Complex

- **Simple**: binary outcome (present/absent) — e.g., `agents-exists`
- **Medium**: 2-3 distinct outcomes or a configurable threshold — e.g., `agents-size`
- **Complex**: multi-path cross-reference logic — e.g., `test-traceability`

### Minimum proof requirement

Every non-`Manual` AC ID must appear in at least one `@pytest.mark.ac("PREFIX-NNN")`
decorator. The `test-coverage` checker warns when fewer than 2 files reference an AC
(i.e., only one of positive or negative is present).
