## Design: change lifecycle checkers

### Shared scanning logic

Both checkers scan `openspec/changes/` (excluding `archive/`). A small helper
`_active_change_dirs(path)` returns the list of subdirectories that are not
the `archive/` folder.

### tasks-complete

Single pass: for each active change dir, read `tasks.md` if it exists. Count
lines matching `- [ ]` (unchecked). If any found, record the folder name.

Result:
- Any unchecked dirs → FAIL, message lists folder names
- No unchecked dirs → PASS

Unchecked pattern: `^- \[ \]` (leading hyphen-space-bracket-space-bracket)
Checked pattern: `^- \[x\]` (case-insensitive for robustness)

### change-archived

Single pass: for each active change dir, read `tasks.md` if it exists. A dir is
**completed** when:
1. `tasks.md` exists
2. At least one task line (`- [ ]` or `- [x]`) is present
3. Zero unchecked `- [ ]` lines remain

Completed dirs that are still under `changes/` (not `archive/`) are flagged.

Result:
- Any completed unarchived dirs → FAIL, message lists folder names
- No completed unarchived → PASS

### Module structure

```
src/iec_cli/checkers/tasks_complete.py
  _UNCHECKED_RE   — matches "- [ ] " lines
  _TASK_RE        — matches any task line (checked or unchecked)
  _active_change_dirs(path) -> list[Path]
  TasksComplete.check(path) -> CheckResult

src/iec_cli/checkers/change_archived.py
  ChangeArchived.check(path) -> CheckResult
  (reuses _active_change_dirs and task regexes from tasks_complete)
```

### No openspec/changes/ directory

If the directory is absent, `_active_change_dirs` returns an empty list and both
checkers return PASS immediately.
