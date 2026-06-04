# tasks-complete Specification

## Purpose

Gate the implementation PR by failing when a change folder's `tasks.md` contains
any unchecked `- [ ]` item. A fully-checked tasks.md (all `- [x]`) signals that
all implementation tasks are done and the change is ready to archive.

---

## Requirements

### Requirement: Active change folder discovery

The checker SHALL scan all direct subdirectories of `openspec/changes/` except
`archive/`. For each subdirectory that contains a `tasks.md` file, the checker
reads that file and counts unchecked items.

#### Scenario: No changes directory present [TSKC-001]

Test-type: Unit

- **WHEN** `openspec/changes/` does not exist
- **THEN** the result is `PASS`

#### Scenario: No tasks.md files found [TSKC-002]

Test-type: Unit

- **WHEN** `openspec/changes/` exists but no change folder contains a `tasks.md`
- **THEN** the result is `PASS`

#### Scenario: All tasks checked [TSKC-003]

Test-type: Unit

- **WHEN** every active change folder's `tasks.md` contains only `- [x]` items
  (no unchecked `- [ ]`)
- **THEN** the result is `PASS`

#### Scenario: Unchecked task in one folder [TSKC-004]

Test-type: Unit

- **WHEN** one change folder's `tasks.md` contains at least one `- [ ]` item
- **THEN** the result is `FAIL` and the change folder name appears in the message

#### Scenario: Multiple folders with unchecked tasks [TSKC-005]

Test-type: Unit

- **WHEN** more than one active change folder's `tasks.md` has unchecked items
- **THEN** the result is `FAIL` and all folder names appear in the message

#### Scenario: Archive subdirectory is skipped [TSKC-006]

Test-type: Unit

- **WHEN** `openspec/changes/archive/` contains folders with unchecked `tasks.md`
- **THEN** those folders are NOT counted and the result does not change to `FAIL`
  on their account

---

### Requirement: Checker registration

The checker SHALL register itself via `@registry.register` with id `"tasks-complete"`.

#### Scenario: Checker is registered [TSKC-007]

Test-type: Unit

- **WHEN** the checkers package is imported
- **THEN** `"tasks-complete"` appears in `registry.list_all()`
