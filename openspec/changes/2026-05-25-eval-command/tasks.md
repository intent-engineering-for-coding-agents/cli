# Tasks: ase eval command

## Implementation

- [x] 1.1 Add `pyyaml>=6` to `pyproject.toml` dependencies; run `uv sync`
- [x] 1.2 Create `src/ase_cli/eval.py` with `EvalCheck`, `EvalTask`, `_run_check`, `_load_tasks`, `run_eval`, `eval_app`
- [x] 1.3 Wire `eval_app` into `src/ase_cli/main.py`

## Tests

- [x] 2.1 Unit tests: `tests/test_eval.py` — `file_exists`, `directory_exists`, `file_contains`, `file_not_contains`, glob, MULTILINE anchor, missing file, unknown type, severity default, `_load_tasks` edge cases
- [x] 2.2 Integration tests: `tests/integration/test_eval.py` — all AC IDs EVAL-001 through EVAL-017

## Example

- [x] 3.1 Create `examples/eval-demo/` with `baseline/`, `after-drift/`, and `eval/` directories
- [x] 3.2 Run `ase eval` on both states; commit output as `score-baseline.txt` and `score-after-drift.txt`

## Verification

- [x] 4.1 `uv run pytest` — 190 tests pass (including new eval tests)
- [x] 4.2 `uv run ruff check . && uv run ruff format --check .` — clean
- [x] 4.3 `ase eval --path examples/eval-demo/baseline --eval-dir examples/eval-demo/eval` — 9/9 (100%)
- [x] 4.4 `ase eval --path examples/eval-demo/after-drift --eval-dir examples/eval-demo/eval` — 5/9 (55%)
