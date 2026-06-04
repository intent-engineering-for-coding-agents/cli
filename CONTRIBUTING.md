# Contributing

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for package management

```bash
git clone https://github.com/intent-engineering-for-coding-agents/cli.git intent-cli
cd intent-cli
uv sync --group dev
```

## Running the CLI from a local checkout

With `uv run`, no installation step is needed — the CLI runs directly from the source tree:

```bash
uv run iec --version
uv run iec check
uv run iec init --dry-run
```

To install the tool globally so `iec` is available without `uv run`:

```bash
uv tool install .
iec --version
```

To verify the install resolves correctly:

```bash
iec --version          # prints version derived from git tag (e.g. 1.0.0)
iec check              # runs all checks on the current directory
```

## Running checks

```bash
uv run ruff check .          # lint
uv run ruff format --check . # format check
uv run pytest                # all tests
uv run iec check             # Intent Engineering self-check
```

## PR taxonomy

All PRs fall into one of three types. Include the type in the PR title:

| Type | When to use | Example title |
|---|---|---|
| `[docs]` | Documentation only, no code | `[docs] Fix typo in README` |
| `[structural]` | Spec, ADR, design doc — no impl code | `[structural] Spec: add foo-check` |
| `[behavior]` | Code changes that alter behaviour | `[behavior] Implement foo-check` |

See [docs/pr-taxonomy.md](docs/pr-taxonomy.md) for the full model and CI gate details.

## Spec-driven workflow

New checkers follow the OpenSpec four-step workflow: **new → plan → apply → archive**.

1. **New**: create a change folder under `openspec/changes/<name>/` with a proposal.
2. **Plan**: fast-forward the proposal into specs, design doc, and tasks.
3. **Apply**: implement the tasks — each must be checkable in `tasks.md`.
4. **Archive**: merge delta specs into `openspec/specs/`, move the change folder to `openspec/changes/archive/<YYYY-MM-DD>-<name>/`.

See [`.agents/instructions/openspec.md`](.agents/instructions/openspec.md) for the full workflow and AC ID conventions.

## Writing tests

Every checker requires:

- A **positive proof** test: the check passes when the condition is met.
- A **negative proof** test: the check fails (or warns) when the condition is violated.
- A `@pytest.mark.<AC_ID>` marker linking the test to its spec scenario.
- A `@pytest.mark.<test_type>` marker (`unit`, `integration`, `sanity`, or `baseline`).

See [docs/testing-convention.md](docs/testing-convention.md) and [`tests/scenario-template.md`](tests/scenario-template.md).

## Adding a new checker

1. Create `src/iec_cli/checkers/<name>.py`. Use an existing checker as a template.
2. Set `id`, `description`, and `maturity` (`Maturity.CI` or `Maturity.ADVISORY`) on the class.
3. Add the module to `src/iec_cli/checkers/__init__.py` (import and `__all__`).
4. Write tests in `tests/test_<name>_checker.py` with AC markers.
5. Add the check to [docs/checks.md](docs/checks.md).

## Maturity labels

Each checker carries a maturity label. See [docs/checks.md](docs/checks.md) for the full catalogue.

- `Maturity.CI` — FAIL on violation; hard CI gate.
- `Maturity.ADVISORY` — WARN on violation; non-blocking in default CI config.
