# Development Guide for ase-cli

This guide documents known issues, best practices, and troubleshooting steps for AI assistants working on this codebase.

## Known Issues & Workarounds

### Typer Help Text Formatting

**Problem:** Tests checking for specific strings in Typer command help output fail on Linux CI but pass on local Windows development.

**Environment:** 
- Fails: Ubuntu 24.04 (GitHub Actions)
- Passes: Windows 11 with Python 3.12.13

**Root Cause:** 
Typer's `CliRunner` help text formatting varies significantly by environment due to:
- Terminal width differences
- ANSI code handling variation
- Typer version behavior differences
- The `@app.callback(invoke_without_command=True)` decorator doesn't reliably display options in all environments

**Original Failing Test:**
```python
def test_check_help() -> None:
    result = runner.invoke(check_app, ["--help"])
    assert result.exit_code == 0
    assert "--path" in result.stdout  # FAILS in CI, passes locally
```

**Solution (Applied):**
Test the actual functionality of the option instead of the help text display:
```python
def test_check_help() -> None:
    result = runner.invoke(check_app, ["--help"])
    assert result.exit_code == 0
    # Verify that the command accepts --path by testing it
    registry.register(_Pass())
    result = runner.invoke(check_app, ["--path", "."])
    assert result.exit_code == 0
    assert "a-ok" in result.stdout
```

**Key Lesson:** Never assert on terminal output formatting. Test functionality instead.

---

## Writing Environment-Agnostic Tests

### 1. Test Functionality, Not Formatting
- ✅ DO: Check that a command produces correct output results
- ❌ DON'T: Assert on specific strings in help output, spacing, colors, or alignment

### 2. Avoid Terminal Output Dependencies
- ✅ DO: Use `result.exit_code` and check for functional output
- ❌ DON'T: Check for `--option-name` in help text, ANSI codes, formatting

### 3. Use CliRunner Correctly
```python
from typer.testing import CliRunner

runner = CliRunner()
result = runner.invoke(app, ["command", "--option", "value"])

# Check what matters
assert result.exit_code == 0  # Command succeeded
assert "expected-output" in result.stdout  # Actual result, not formatting
```

### 4. For CLI Options Verification
Instead of:
```python
result = runner.invoke(app, ["--help"])
assert "--myoption" in result.stdout  # Fragile, environment-dependent
```

Do this:
```python
# Test that the option actually works
result = runner.invoke(app, ["--myoption", "value"])
assert result.exit_code == 0
assert "expected-behavior" in result.stdout
```

---

## CI Maintenance Workflow

### When Workflows Fail

1. **Identify Failure Type**
   - Code/test failure: Check `pytest` output for specific assertion failures
   - Action failure: Check GitHub Actions logs for setup/environment issues
   - Linting failure: Check `ruff` output for specific violations

2. **Check for Environment-Specific Issues**
   - Note the OS and Python version from CI logs
   - Check if test passes locally
   - Look for terminal output assertions (likely culprit)

3. **Search History**
   ```bash
   git log --oneline --all -- <affected-file>
   git show <commit>:<affected-file>  # See what changed
   ```

4. **Document Findings**
   - Add to this file if it's a new pattern
   - Update related test comments with workaround details

### Debugging Failed Workflows

Check the full CI logs:
```bash
gh run list --repo ase-book/ase-cli --limit 1
gh run view <run-id> --log --repo ase-book/ase-cli
```

Look for:
- Python version running
- Specific assertion that failed
- Any error messages from dependencies
- Terminal/formatting-related output

---

## Architecture Notes

### CLI Structure
- `main.py`: Entry point, adds check_app and init command to main app
- `check.py`: Check command logic using `@check_app.callback(invoke_without_command=True)`
- `check_app` is added to main app as a sub-app: `app.add_typer(check_app, name="check")`

**Important:** The callback decorator is required because check_app is a sub-app. Don't change to `@check_app.command()` as it breaks the command invocation structure.

### Test Organization
- `tests/integration/`: End-to-end tests with real checkers and CLI
- `tests/`: Unit tests for individual components
- `tests/integration/test_check.py`: Tests for check command functionality (not help text)

---

## Typer Version Constraint

Current: `typer>=0.15`

**Note:** This is a loose constraint. If environment-specific issues reoccur, consider pinning to a tested version:
```toml
typer>=0.15,<0.26  # Tested range
```

Monitor: https://github.com/tiangolo/typer/releases

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| `--help` test fails on CI but passes locally | Don't test help text. Test option functionality instead. |
| Tests pass locally, fail on CI | Check for environment assumptions (os, terminal, Python version) |
| New Typer version breaks tests | See if help text assertions are involved; use functionality tests instead. |
| Linting fails | Run `uv run ruff check .` and `uv run ruff format .` locally first |
| Tests fail on import | Run `uv sync` to ensure dependencies are installed |

---

## Useful Commands

```bash
# Run tests
uv run pytest                          # All tests
uv run pytest tests/integration/       # Only integration tests
uv run pytest tests/test_check.py -xvs # Single file, verbose, stop on first failure

# Linting
uv run ruff check .                    # Check for issues
uv run ruff format .                   # Auto-format

# Check actual CLI
uv run ase check --help
uv run ase init --help
```

