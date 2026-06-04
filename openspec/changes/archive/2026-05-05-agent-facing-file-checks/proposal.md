# Proposal: Agent-Facing File Checks

## Why

Every Intent Engineering repo needs an AGENTS.md. Its presence, size, and link quality determine whether coding agents receive useful context or drift. The check framework from Change 002 can run checkers, but no checkers exist yet. These three are the first — they validate the most critical agent-facing file.

## What Changes

- **`agents-exists` checker**: Validates `AGENTS.md` exists at the repo root. Returns PASS if found, FAIL if missing.
- **`agents-size` checker**: Validates `AGENTS.md` is under a configurable line limit (default 50). Returns FAIL if over the limit, PASS otherwise.
- **`agents-links` checker**: Validates every Markdown link in `AGENTS.md` is followed by descriptive text — not a bare URL or naked path. A bare link is a link-only list item with no trailing description (e.g., `- [file.md](file.md)` followed by nothing). Returns WARN for each bare link found.
- Each checker is a class conforming to the `Checker` protocol, registered via `@registry.register`.
- No modifications to existing specs.

## Capabilities

### New Capabilities

- `agents-exists`: Checks that `AGENTS.md` is present at the repo root. FAIL if missing.
- `agents-size`: Checks that `AGENTS.md` is under a configurable line limit (default: 50). FAIL if exceeded.
- `agents-links`: Checks that every link in `AGENTS.md` is followed by descriptive text. WARN for each bare link.

### Modified Capabilities

*(None — all existing specs unchanged)*

## Impact

- **New module**: `src/iec_cli/checkers/` package with `__init__.py` and three checker modules
- **`src/iec_cli/check.py`**: `_load_checkers()` imports the new checker modules so they self-register
- **Tests**: Unit tests per checker (file I/O with tmp_path), integration tests for `iec check` with real checkers
- **No new dependencies**: All checks are file I/O + regex, pure Python
- **No breaking changes**: `iec check` runs existing checkers plus new ones transparently
