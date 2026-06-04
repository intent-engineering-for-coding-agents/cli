# Build and CI

## Local Development

```
uv sync --group dev     # Install dependencies (first time + after changes)
uv run ruff check .     # Lint
uv run ruff format .    # Format
uv run pytest           # Test
```

Never install without `--group dev` — runtime deps (typer) are needed, dev deps (ruff, pytest) are needed for development.

## CI Pipeline

GitHub Actions (`.github/workflows/ci.yml`) runs on every push and PR to `main`:

| Job | Python | What it runs |
|---|---|---|
| lint | 3.12 | `ruff check`, `ruff format --check` |
| test | 3.12, 3.13 | `pytest` |

CI uses `astral-sh/setup-uv@v5` with `python-version`. No pip, no virtualenv manual management.

## Adding a Dependency

1. Add to `pyproject.toml` under `dependencies` (runtime) or `[dependency-groups] dev` (dev-only)
2. Run `uv sync --group dev` — uv resolves and updates the lockfile
3. Commit both `pyproject.toml` and `uv.lock` (if checked in)

## Self-Validation

In Phase H, CI will also run `iec check --deterministic` on the repo itself — the tool validates its own practices. Until then, manual compliance with all ADRs is expected.

## Version Tagging

Version is derived automatically from git tags via `hatch-vcs`. **Do not edit `version` in `pyproject.toml`** — there is none.

To cut a release:

```
git tag v0.7.0
git push origin v0.7.0
```

That's it. `iec --version` will return `0.7.0` on the next build. Between tags, the version looks like `0.6.0.dev3+gabcdef1` (commits since last tag).

CI fetches full git history (`fetch-depth: 0`) so tag resolution works in GitHub Actions.
