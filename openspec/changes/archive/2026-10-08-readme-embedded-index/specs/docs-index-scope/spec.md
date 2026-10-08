## ADDED Requirements

### Requirement: Embedded README index block stays within scope

For a directory without `INDEX.md` whose `README.md` contains an index block, the `docs-index-scope` checker SHALL apply the same link rules to the links between the markers. Links elsewhere in the README SHALL be ignored. Offenders are reported as `<dir>/README.md -> <target>`.

#### Scenario: Deeper path inside a README.md block [DISO-009]

Test-type: unit

- **WHEN** the block in `docs/README.md` contains `[ADR](decisions/0001-x.md)`
- **THEN** the result is `WARN` and the message lists `docs/README.md -> decisions/0001-x.md`

#### Scenario: Links outside the block are ignored [DISO-010]

Test-type: unit

- **WHEN** `docs/README.md` has `[the guide](../guide/start.md)` in prose above a terminated block with only in-scope rows
- **THEN** the result is `PASS`

#### Scenario: Child README.md pointer inside a block [DISO-011]

Test-type: unit

- **WHEN** the block in `docs/README.md` contains `[Decisions](decisions/README.md)`
- **THEN** the result is `PASS`
