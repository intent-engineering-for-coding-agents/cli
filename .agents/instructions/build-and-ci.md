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

When a phase completes and a new tag is created, the version in `pyproject.toml` MUST be bumped to match:

1. Update `version = "..."` in `pyproject.toml` (top-level `[project]` table)
2. Run `uv sync` to regenerate the lockfile
3. Create the git tag: `git tag vX.Y.Z && git push origin vX.Y.Z`
4. Commit the version bump as a separate commit before or with the tag

`iec --version` reads from `pyproject.toml` via `importlib.metadata.version()`. A tag without a matching version in `pyproject.toml` is broken.
