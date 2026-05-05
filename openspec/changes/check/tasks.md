# Tasks: Deterministic Check Framework

## 1. Check Result Model

- [ ] 1.1 Define `Status` enum (PASS, WARN, FAIL) in `src/ase_cli/check.py`
- [ ] 1.2 Define `Severity` enum (HIGH, MEDIUM, LOW) in `src/ase_cli/check.py`
- [ ] 1.3 Define `CheckResult` dataclass with all fields (`check_id`, `status`, `message`, `severity`, `location=None`, `ac_id=None`) in `src/ase_cli/check.py`
- [ ] 1.4 Add `is_warning` and `is_failure` properties to `CheckResult`

## 2. Checker Registry

- [ ] 2.1 Define `Checker` protocol with `id`, `description`, and `check(path: Path) -> CheckResult` in `src/ase_cli/check.py`
- [ ] 2.2 Implement `Registry` class with `_checkers` dict, `register(checker)` method, `list_all()` method in `src/ase_cli/check.py`
- [ ] 2.3 Ensure `register()` raises `TypeError` for non-conforming objects (missing `id` or `check`)
- [ ] 2.4 Ensure `register()` is idempotent — same checker ID registered twice is a no-op
- [ ] 2.5 Implement `run_all(path: Path) -> list[CheckResult]` — runs all checkers, catches exceptions, returns results
- [ ] 2.6 Implement `run_one(check_id: str, path: Path) -> CheckResult` — runs single checker by ID, raises `KeyError` for unknown
- [ ] 2.7 Create module-level `registry` instance for decorator and CLI access

## 3. CLI Command

- [ ] 3.1 Create `check_app` Typer instance in `src/ase_cli/check.py`
- [ ] 3.2 Implement `ase check` command: accepts `--path` argument (default `.`), calls `registry.run_all()`
- [ ] 3.3 Implement result formatting function — per-checker lines with status and message
- [ ] 3.4 Implement summary output — total count, pass/warn/fail breakdown
- [ ] 3.5 Implement exit code logic: 0 = all pass, 1 = warnings (no failures), 2 = failures
- [ ] 3.6 Wire `check_app` into `src/ase_cli/main.py` via `app.add_typer()`
- [ ] 3.7 Add `_load_checkers()` function (empty body, placeholder for Change 003+)

## 4. Tests

- [ ] 4.1 Unit tests for `Status` and `Severity` enums — all values present [CHKRSL-001, CHKRSL-002]
- [ ] 4.2 Unit tests for `CheckResult` construction — all fields, minimal fields, equality [CHKRSL-003, CHKRSL-004, CHKRSL-005]
- [ ] 4.3 Unit tests for `CheckResult` helper properties [CHKRSL-006, CHKRSL-007]
- [ ] 4.4 Unit tests for checker registration — register, duplicate rejection, `TypeError` on non-conforming [CHKREG-001, CHKREG-002, CHKREG-003]
- [ ] 4.5 Unit tests for `Checker` protocol conformance [CHKREG-004]
- [ ] 4.6 Unit tests for `run_all()` — all pass, one fail, exception handling, empty registry [CHKREG-005, CHKREG-006, CHKREG-007, CHKREG-008]
- [ ] 4.7 Unit tests for `run_one()` — existing checker, unknown checker [CHKREG-009, CHKREG-010]
- [ ] 4.8 Unit tests for `list_all()` — returns registration order [CHKREG-011]
- [ ] 4.9 Integration tests for `ase check` CLI — default path, `--path` flag, `--help` [CHKCLI-001, CHKCLI-002, CHKCLI-003]
- [ ] 4.10 Integration tests for CLI exit codes — 0, 1, 2 [CHKCLI-007, CHKCLI-008, CHKCLI-009]
- [ ] 4.11 Integration tests for CLI output — all pass, one fail, mixed results, ordering [CHKCLI-004, CHKCLI-005, CHKCLI-006, CHKCLI-010]

## 5. Verify

- [ ] 5.1 Run `uv run ruff check` — no lint errors
- [ ] 5.2 Run `uv run ruff format --check` — no formatting issues
- [ ] 5.3 Run `uv run pytest -v` — all tests pass (CHKREG: 11, CHKRSL: 7, CHKCLI: 10 = 28 AC IDs)
- [ ] 5.4 Run `uv run pytest --cov=src/ase_cli/check --cov-report=term-missing` — verify coverage
- [ ] 5.5 Run `ase --help` — `check` command appears in output
