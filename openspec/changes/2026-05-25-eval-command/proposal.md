# Proposal: iec eval command

## Why

The `iec check` command validates static structural properties of a repo. There is no equivalent for validating agent output: the code and tests an agent produces after receiving an instruction. Without a way to compare agent output across two configurations of `AGENTS.md`, teams cannot detect the quiet drift the Intent Engineering for Coding Agents describes — a change that looks harmless and shifts the codebase over days.

`iec eval` closes that loop. It reads a directory of eval tasks, each with a `task.md` (what to give the agent) and a `checks.yaml` (properties to verify after the agent runs). It checks filesystem state, counts passes and failures per task, and prints a score table. The agent runs manually; the CLI checks the result.

## What changes

- **New subcommand `iec eval`**: `src/iec_cli/eval.py` with `EvalCheck`, `EvalTask`, `_run_check`, `_load_tasks`, `run_eval`, and `eval_app`.
- **`src/iec_cli/main.py`**: Wire `eval_app` as `app.add_typer(eval_app, name="eval")`.
- **`pyproject.toml`**: Add `pyyaml>=6` to `[project.dependencies]`.
- **`examples/eval-demo/`**: A self-contained A/B example showing baseline (9/9, 100%) and after-drift (5/9, 55%) states with pre-committed score files.
- **Tests**: `tests/test_eval.py` (unit) and `tests/integration/test_eval.py`.

## Capabilities

### New capabilities

- `iec eval [--path PATH] [--eval-dir EVAL_DIR]`: Run a YAML-driven eval suite against a repo state. Supported check types: `file_exists`, `directory_exists`, `file_contains`, `file_not_contains`. Outputs a score table per task plus a total. Exits 0 (all pass), 1 (warnings), or 2 (failures).

### Modified capabilities

- `iec` help output now lists `eval` alongside `check` and `init`.

## Impact

- No changes to existing checkers, Registry, or `iec check`.
- One new external dependency: `pyyaml>=6`.
- `examples/eval-demo/` is not part of the installed package; it is a standalone directory for demonstration.
