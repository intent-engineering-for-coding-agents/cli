# Tasks: change-lifecycle (Change 011)

## 1. tasks-complete — implementation

- [x] 1.1 Create `src/iec_cli/checkers/tasks_complete.py` with `TasksComplete` class registered via `@registry.register`
- [x] 1.2 Implement `_active_change_dirs(path)` helper — returns active change subdirs excluding `archive/`
- [x] 1.3 Implement task scanning: count unchecked `- [ ]` lines in each `tasks.md`

## 2. change-archived — implementation

- [x] 2.1 Create `src/iec_cli/checkers/change_archived.py` with `ChangeArchived` class registered via `@registry.register`
- [x] 2.2 Implement completion detection: tasks.md exists, has at least one task line, all checked

## 3. tasks-complete — proof

- [x] 3.1 Positive: no changes dir → PASS [TSKC-001]
- [x] 3.2 Positive: no tasks.md files → PASS [TSKC-002]
- [x] 3.3 Positive: all tasks checked → PASS [TSKC-003]
- [x] 3.4 Negative: unchecked task in one folder → FAIL with name [TSKC-004]
- [x] 3.5 Negative: multiple folders with unchecked → all names reported [TSKC-005]
- [x] 3.6 Edge: archive/ subdir skipped [TSKC-006]
- [x] 3.7 Registration [TSKC-007]

## 4. change-archived — proof

- [x] 4.1 Positive: no changes dir → PASS [CHGA-001]
- [x] 4.2 Positive: no active change folders → PASS [CHGA-002]
- [x] 4.3 Positive: in-progress change (unchecked tasks) → PASS [CHGA-003]
- [x] 4.4 Negative: completed not archived → FAIL with name [CHGA-004]
- [x] 4.5 Negative: multiple completed unarchived → all names [CHGA-005]
- [x] 4.6 Edge: no tasks.md → not flagged [CHGA-006]
- [x] 4.7 Registration [CHGA-007]

## 5. Wiring

- [x] 5.1 Import both modules in `src/iec_cli/checkers/__init__.py`
- [x] 5.2 Add `tasks-complete` and `change-archived` assertions to integration test

## 6. Verify

- [x] 6.1 `uv run ruff check` — no lint errors
- [x] 6.2 `uv run ruff format --check` — no formatting issues
- [x] 6.3 `uv run pytest -v` — all 14 new ACs proven, full suite passes
