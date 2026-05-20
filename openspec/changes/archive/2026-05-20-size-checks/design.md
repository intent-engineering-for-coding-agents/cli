# Design: File and Spec Size Checks

## spec-size

Uses `find_spec_files(path)` from `_shared.py`. Reads each file, counts `splitlines()`. Returns `WARN` (not `FAIL`) — size is advisory.

Env `ASE_SPEC_MAX_LINES`: parsed with `int()`, falls back to 500 on `ValueError` or when unset.

## file-size

Walks `path.rglob("*.md")`. Skips any entry whose path components include `.git`, `node_modules`, `.venv`, `venv`, `__pycache__`, or `.vitepress`. Counts lines per file, returns WARN for violations.

Env `ASE_FILE_MAX_LINES`: same fallback logic as `spec-size`.

## Severity

`Severity.MEDIUM` — size is a code smell, not a structural failure. WARN exit code (1) does not block CI by default.
