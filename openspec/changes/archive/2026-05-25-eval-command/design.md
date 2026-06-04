# Design: iec eval command

## Approach

`iec eval` is a separate Typer sub-app (`eval_app`) wired into `main.py` alongside `check_app`. It does not touch the Registry or registered checkers — eval tasks are runtime-loaded from YAML per invocation, not statically registered.

## Data model

```
EvalCheck
  id: str
  description: str
  type: str          # file_exists | directory_exists | file_contains | file_not_contains
  path: str | None   # for file_exists, directory_exists — glob patterns supported
  file: str | None   # for file_contains, file_not_contains
  pattern: str | None
  severity: Severity = Severity.HIGH

EvalTask
  name: str          # directory name
  checks: list[EvalCheck]
```

`CheckResult`, `Status`, and `Severity` are reused from `iec_cli.check` unchanged.

## Check dispatch

`_run_check(check, root)` dispatches on `check.type`:

- `file_exists`: `glob.glob(str(root / check.path))` — PASS if any match, FAIL if none. Glob patterns allow `docs/*.md` style checks.
- `directory_exists`: `(root / check.path).is_dir()`.
- `file_contains`: read file as UTF-8, `re.search(check.pattern, content, re.MULTILINE)` — PASS if match found. **`re.MULTILINE` is required** so that `^` in patterns like `^class ` anchors to line starts, not the start of the entire file.
- `file_not_contains`: inverse of `file_contains`.
- Unknown type: FAIL with `"unknown check type: {type}"`.
- Missing file (for `file_contains`/`file_not_contains`): FAIL with `"file not found: {path}"`.

## Task discovery

`_load_tasks(eval_dir)` walks `eval_dir`, sorted, filtering to subdirectories containing `checks.yaml`. Each `checks.yaml` is parsed with `yaml.safe_load`. Malformed YAML produces a single FAIL `CheckResult` for the task rather than crashing.

## Path resolution

When `--eval-dir` is a relative path, it is resolved relative to `--path` (the repo root), not the process working directory. This allows `iec eval --path baseline --eval-dir eval` to find `baseline/../eval` naturally when called from the demo directory. Absolute paths bypass this resolution.

## Output

Score table with fixed columns (30 chars task name, 4 chars per count). Separator is ASCII `-` for cross-platform compatibility. Score line: `Score: X/N (PCT%)`. Failures block lists only FAIL results, one per line with format `  {task.name} / {check_id}: {message}`.

## Dependency: PyYAML

Python's stdlib has no YAML parser. `yaml.safe_load` from PyYAML is safe (no arbitrary object construction) and handles the multi-key, nested-list structure of `checks.yaml` cleanly. `tomllib` (stdlib, 3.11+) only reads TOML.

## Why not reuse the Registry

The Registry holds statically registered checker classes with a fixed lifecycle. Eval checks are runtime-loaded from YAML files per invocation and have no stable ID outside a given eval directory. Mixing them would require either a second Registry with reset semantics or contaminating `iec check`'s registered checker set.
