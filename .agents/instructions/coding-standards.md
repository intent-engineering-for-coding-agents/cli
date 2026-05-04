# Coding Standards

## Python Style

- **Type hints** on all function signatures — no exceptions
- **Double quotes** for strings (enforced by ruff format)
- **No comments** unless explaining *why*, not *what*
- **No print()** — use `typer.echo()` or `rich` for output

## Project Structure

```
src/ase_cli/
├── main.py          # Typer app entry point
├── checks/          # Check implementations (plugin registry)
│   └── __init__.py
├── mcp_server.py    # MCP server (Phase F)
└── generators/      # Vendor file generators (Phase G)
    └── __init__.py

tests/
├── test_checks/
└── test_generators/
```

Mirror `src/` structure in `tests/`. One test file per source module.

## Linting

Ruff is configured in `pyproject.toml`. Run before committing:

```
uv run ruff check .       # Lint
uv run ruff format .      # Format
```

Rules selected: `E` (pycodestyle), `F` (pyflakes), `I` (isort), `N` (pep8-naming), `W` (warnings), `UP` (pyupgrade).

No additional linters. Ruff is the single lint/format tool.

## Testing

pytest with standard conventions:

- Test files prefixed `test_`
- Test functions prefixed `test_`
- Use `@pytest.mark.ac("ID")` for AC traceability
- Every check module gets positive + negative test cases
- Run: `uv run pytest`
