## ADDED Requirements

### Requirement: Embedded README index block cross-reference

When a directory has no `INDEX.md` and its `README.md` contains an index block, the `docs-index-stale` checker SHALL treat the lines between the markers as the index: links are resolved relative to the directory, referenced files that do not exist are broken links, and other files in the directory are orphans. `README.md` itself SHALL NOT be reported as an orphan. Links outside the block SHALL be ignored. When `INDEX.md` exists, it SHALL be used and the README block ignored.

#### Scenario: README.md block matches the directory [DINS-008]

Test-type: unit

- **WHEN** `docs/README.md` has a block listing `a.md`, a prose link to a missing file outside the block, and `docs/a.md` exists
- **THEN** the result is `PASS`

#### Scenario: Orphan next to a README.md block [DINS-009]

Test-type: unit

- **WHEN** `docs/b.md` exists but the block in `docs/README.md` lists only `a.md`
- **THEN** the result is `WARN` and the message lists `docs/b.md`

#### Scenario: Broken link inside a README.md block [DINS-010]

Test-type: unit

- **WHEN** the block in `docs/README.md` links `gone.md`, which does not exist
- **THEN** the result is `WARN` and the message lists `gone.md`

#### Scenario: INDEX.md wins over a README.md block [DINS-011]

Test-type: unit

- **WHEN** `docs/` has an accurate `INDEX.md` and `docs/README.md` has a block linking `nope.md`
- **THEN** the result is `PASS`
