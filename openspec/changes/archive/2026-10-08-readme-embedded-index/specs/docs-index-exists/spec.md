## ADDED Requirements

### Requirement: Embedded README index block satisfies the presence rule

A `docs/` directory SHALL also count as having an index when its `README.md` contains an index block: a line `<!-- index:start -->`, followed later by a line `<!-- index:end -->`. This extends the INDEX.md presence rule. A start marker with no closing marker SHALL NOT count.

#### Scenario: README.md with an index block counts [DINE-007]

Test-type: unit

- **WHEN** `docs/` has no `INDEX.md` and `docs/README.md` contains a terminated index block
- **THEN** the result is `PASS`

#### Scenario: README.md without an index block does not count [DINE-008]

Test-type: unit

- **WHEN** `docs/` has no `INDEX.md` and `docs/README.md` has no index markers
- **THEN** the result is `WARN` and the message lists `docs`

#### Scenario: Unterminated index block does not count [DINE-009]

Test-type: unit

- **WHEN** `docs/README.md` contains `<!-- index:start -->` with no `<!-- index:end -->`
- **THEN** the result is `WARN`
