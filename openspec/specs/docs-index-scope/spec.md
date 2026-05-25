# docs-index-scope Specification

## Purpose

Each `INDEX.md` is a *flat* map of its own directory. The checker enforces this so that documents form a hypergraph navigated by following sub-INDEX pointers, not a tree collapsed into a single master index. Without it, top-level indexes accumulate per-file rows from sub-directories and drift silently — `docs-index-stale` only validates each INDEX against its own directory contents and cannot catch out-of-scope entries.

## Requirements

### Requirement: INDEX.md links stay within the directory's own scope

The system SHALL provide a `docs-index-scope` checker that walks the `docs/` directory tree. For every `INDEX.md` found, the checker SHALL parse Markdown inline links `[text](target)` and verify that each `target` is either (a) a same-directory file (no `/` in the path), or (b) an immediate child pointer matching `^[^/]+/(INDEX|README)\.md$`. Targets that are deeper paths, parent paths (`../`), or absolute URLs SHALL be flagged. The checker SHALL return PASS when all INDEX links are in scope, and WARN listing every offender as `<rel-dir>/INDEX.md -> <target>`.

#### Scenario: Same-directory file link [DISO-001]

Test-type: unit

- **WHEN** `docs/INDEX.md` contains `[A](a.md)` and `docs/a.md` exists
- **THEN** the result is `PASS`

#### Scenario: Immediate subdir INDEX.md pointer [DISO-002]

Test-type: unit

- **WHEN** `docs/INDEX.md` contains `[Decisions](decisions/INDEX.md)`
- **THEN** the result is `PASS`

#### Scenario: Immediate subdir README.md pointer [DISO-003]

Test-type: unit

- **WHEN** `docs/INDEX.md` contains `[Decisions](decisions/README.md)`
- **THEN** the result is `PASS`

#### Scenario: Deeper path is out of scope [DISO-004]

Test-type: unit

- **WHEN** `docs/INDEX.md` contains `[ADR-0001](decisions/0001-x.md)`
- **THEN** the result is `WARN` and the message lists `decisions/0001-x.md`

#### Scenario: Parent path is out of scope [DISO-005]

Test-type: unit

- **WHEN** `docs/INDEX.md` contains `[Agents](../AGENTS.md)`
- **THEN** the result is `WARN` and the message lists `../AGENTS.md`

#### Scenario: Absolute URL is out of scope [DISO-006]

Test-type: unit

- **WHEN** `docs/INDEX.md` contains `[External](https://example.com/x)`
- **THEN** the result is `WARN` and the message lists the URL

#### Scenario: Directories without INDEX.md are skipped [DISO-007]

Test-type: unit

- **WHEN** a `docs/` subdirectory has no `INDEX.md`
- **THEN** the checker does not inspect it and does not report it (presence is the job of `docs-index-exists`)

### Requirement: checker registration

The checker SHALL register itself via `@registry.register` with `id` `"docs-index-scope"`.

#### Scenario: Checker is registered [DISO-008]

Test-type: unit

- **WHEN** the checkers package is imported
- **THEN** `"docs-index-scope"` appears in `registry.list_all()`
