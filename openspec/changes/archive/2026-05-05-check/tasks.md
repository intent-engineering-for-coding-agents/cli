# Tasks: Deterministic Check Framework

## 1. Check Result Model — implementation and proof

- [x] 1.1 Define `Status` enum (PASS, WARN, FAIL) and `Severity` enum (HIGH, MEDIUM, LOW) in `src/iec_cli/check.py`, with positive + negative unit tests for all enum values [CHKRSL-001, CHKRSL-002]
- [x] 1.2 Define `CheckResult` dataclass with all fields (`check_id`, `status`, `message`, `severity`, `location=None`, `ac_id=None`) and `is_warning`/`is_failure` properties in `src/iec_cli/check.py`
- [x] 1.3 Positive + negative unit tests for `CheckResult` — construction with all fields, construction with minimal fields (None defaults), equality comparison, and helper properties [CHKRSL-003, CHKRSL-004, CHKRSL-005, CHKRSL-006, CHKRSL-007]

## 2. Checker Protocol — definition and proof

- [x] 2.1 Define `Checker` protocol with `id`, `description`, and `check(path: Path) -> CheckResult` in `src/iec_cli/check.py`
- [x] 2.2 Positive + negative unit tests: conforming class satisfies protocol, non-conforming class (missing `id` or `check`) does not [CHKREG-004]

## 3. Registry implementation and proof

- [x] 3.1 Implement `Registry` class with `_checkers` dict, `register(checker)` method, and `list_all()` method in `src/iec_cli/check.py`
- [x] 3.2 Positive + negative unit tests for `register()`: success (positive), `TypeError` on missing `id`/`check` (negative), duplicate registration is idempotent (boundary) [CHKREG-001, CHKREG-002, CHKREG-003]
- [x] 3.3 Positive unit test for `list_all()`: returns `(id, description)` tuples in registration order [CHKREG-011]
- [x] 3.4 Implement `run_all(path: Path) -> list[CheckResult]` — runs all checkers in registration order, catches exceptions, returns results for all
- [x] 3.5 Positive + negative unit tests for `run_all()`: all checkers pass (positive), one fails others continue (negative), unexpected exception caught and reported (negative), empty registry (boundary) [CHKREG-005, CHKREG-006, CHKREG-007, CHKREG-008]
- [x] 3.6 Implement `run_one(check_id: str, path: Path) -> CheckResult` — runs single checker by ID, raises `KeyError` for unknown IDs
- [x] 3.7 Positive + negative unit tests for `run_one()`: runs existing checker (positive), raises `KeyError` for unknown ID (negative) [CHKREG-009, CHKREG-010]
- [x] 3.8 Create module-level `registry` instance for decorator and CLI access

## 4. CLI command — implementation and proof

- [x] 4.1 Create `check_app` Typer instance and implement `iec check` command with `--path` argument (default `.`) in `src/iec_cli/check.py`
- [x] 4.2 Positive + negative integration tests for CLI entry: runs with default path (positive), runs with `--path` (positive), `--help` shows options (positive), non-existent path (negative) [CHKCLI-001, CHKCLI-002, CHKCLI-003]
- [x] 4.3 Implement result formatting — per-checker lines (PASS/WARN/FAIL with message) and summary output (total count, breakdown) — plain text, no colors
- [x] 4.4 Positive + negative integration tests for output: all checks pass (positive), one check fails (negative), mixed PASS/WARN/FAIL (negative), results follow registration order (boundary) [CHKCLI-004, CHKCLI-005, CHKCLI-006, CHKCLI-010]
- [x] 4.5 Implement exit codes: 0 (all pass), 1 (warnings, no failures), 2 (failures)
- [x] 4.6 Positive + negative integration tests for exit codes: all pass → 0 (positive), warnings only → 1 (positive), failures → 2 (negative) [CHKCLI-007, CHKCLI-008, CHKCLI-009]
- [x] 4.7 Wire `check_app` into `src/iec_cli/main.py` via `app.add_typer()` and add `_load_checkers()` placeholder function
- [x] 4.8 Integration smoke test: `iec --help` lists `check` command

## 5. Verify

- [x] 5.1 Run `uv run ruff check` — no lint errors
- [x] 5.2 Run `uv run ruff format --check` — no formatting issues
- [x] 5.3 Run `uv run pytest -v` — all 28 AC IDs proven (CHKREG 11, CHKRSL 7, CHKCLI 10)
- [x] 5.4 Run `uv run pytest --cov=src/iec_cli/check --cov-report=term-missing` — verify coverage
