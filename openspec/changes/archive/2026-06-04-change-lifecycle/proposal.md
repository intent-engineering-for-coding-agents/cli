## Why

The OpenSpec workflow requires two lifecycle gates to be enforced deterministically:
a change folder should not be merged with incomplete tasks, and a fully-completed
change folder should not linger on trunk without being archived. Without these checks,
dead-spec drift accumulates silently — tasks.md shows all green but the delta specs
never merge into openspec/specs/, and the change folder stays live indefinitely.

## What Changes

- New checker `tasks-complete`: scans every change folder under `openspec/changes/`
  (excluding `archive/`) for a `tasks.md` file and fails when any unchecked `- [ ]`
  item is found. Gate for the implementation PR.
- New checker `change-archived`: scans for change folders whose `tasks.md` is fully
  checked but that have not yet been moved to `changes/archive/`. Fires the
  "finished but not archived" dead-spec warning the book describes.

## Capabilities

### New Capabilities

- `tasks-complete`: Fail when any active change folder's tasks.md has unchecked items.
- `change-archived`: Fail when a fully-completed change folder is not yet archived.

### Modified Capabilities

(none)

## Impact

- New files: `src/iec_cli/checkers/tasks_complete.py`, `src/iec_cli/checkers/change_archived.py`
- Update: `src/iec_cli/checkers/__init__.py`
- New test file: `tests/test_lifecycle_checkers.py`
