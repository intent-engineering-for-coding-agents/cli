# change-archived Specification

## Purpose

Detect the "finished but not archived" dead-spec state: a change folder under
`openspec/changes/` whose `tasks.md` is fully checked but which has not been moved
to `changes/archive/`. The book describes this as the primary source of long-lived
stale specs on trunk.

---

## Requirements

### Requirement: Completed change detection

The checker SHALL scan all direct subdirectories of `openspec/changes/` except
`archive/`. A change folder is considered **completed** when its `tasks.md` exists
and contains at least one task line (`- [ ]` or `- [x]`) and all task lines are
checked (`- [x]`). A completed change that is still under `changes/` (not yet in
`archive/`) SHALL produce a `FAIL` result.

#### Scenario: No changes directory present [CHGA-001]

Test-type: Unit

- **WHEN** `openspec/changes/` does not exist
- **THEN** the result is `PASS`

#### Scenario: No active change folders [CHGA-002]

Test-type: Unit

- **WHEN** `openspec/changes/` exists but contains no subdirectories other than `archive/`
- **THEN** the result is `PASS`

#### Scenario: Change in progress — unchecked tasks [CHGA-003]

Test-type: Unit

- **WHEN** a change folder's `tasks.md` contains at least one unchecked `- [ ]` item
- **THEN** the change is NOT considered completed and the result is `PASS`
  (tasks-complete handles this gate)

#### Scenario: Completed change not archived [CHGA-004]

Test-type: Unit

- **WHEN** a change folder's `tasks.md` exists and all task lines are `- [x]`
- **THEN** the result is `FAIL` and the change folder name appears in the message

#### Scenario: Multiple completed unarchived changes [CHGA-005]

Test-type: Unit

- **WHEN** more than one active change folder is completed but not archived
- **THEN** the result is `FAIL` and all folder names appear in the message

#### Scenario: No tasks.md — change not considered completed [CHGA-006]

Test-type: Unit

- **WHEN** a change folder has no `tasks.md` file
- **THEN** the folder is NOT flagged as completed and does not affect the result

---

### Requirement: Checker registration

The checker SHALL register itself via `@registry.register` with id `"change-archived"`.

#### Scenario: Checker is registered [CHGA-007]

Test-type: Unit

- **WHEN** the checkers package is imported
- **THEN** `"change-archived"` appears in `registry.list_all()`
