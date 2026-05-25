# ase-cli Testing Strategy

> Concrete instantiation of `docs/testing-convention.md` for this project.

---

## Applicable Test Layers

| Layer | Category | Applies? | What it means here |
|---|---|---|---|
| L1 | `Unit` | Yes | Pure Python functions — individual checkers, scaffolding logic, utilities. No I/O, no CLI invocation. |
| L2 | `Slice` | No | Not applicable. ase-cli is a CLI tool, not a web framework. No sliced test context equivalent. |
| L3 | `Integration` | Yes | Invoke `ase` commands via `typer.testing.CliRunner` against real temporary directories. Test filesystem scaffolding, flag behavior, exit codes. |
| L4 | `E2E` | No | No service boundaries to cross. Reserved for future MCP server workflow tests. |
| L5 | `Performance` | No | Not needed. CLI tool operations are sub-second. |

| Category | Applies? | What it means here |
|---|---|---|
| `Baseline` | Yes | Tests that exist to satisfy coverage thresholds for non-AC code paths. Mark with `@pytest.mark.baseline`. |
| `Architectural` | No | No ArchUnit/NetArchTest equivalent in Python. Ruff lint checks serve this role in CI. |
| `Manual` | Yes | Manual verification steps that cannot be automated (e.g., "verify CLI output is readable in a terminal"). |
| `Sanity` | Yes | Environment checks — package importable, Typer app exists, Python version. |

---

## AC ID Format

Prefixes map to capability names in `openspec/specs/<capability>/`:

| Capability | Prefix |
|---|---|
| `scaffold-command` | `SCAFFOLD` |
| `vendor-generators` | `VENDOR` |
| `check-framework` (future) | `CHECK` |

Example scenario:
```markdown
#### Scenario: Init in empty directory [SCAFFOLD-001]

Test-type: integration
```

---

## Traceability Markers

```python
# AC-tagged test
@pytest.mark.ac("SCAFFOLD-001")
def test_init_creates_all_dirs_and_files(tmp_path):
    ...

# Non-AC markers
@pytest.mark.baseline
def test_coverage_for_unreachable_branch():
    ...

@pytest.mark.sanity
def test_package_importable():
    ...
```

Registered in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
markers = [
    "ac: marks a test as proving a specific acceptance criterion",
    "baseline: marks coverage threshold or structural regression tests",
    "sanity: marks environment or toolchain readiness tests",
]
```

---

## Test Directory Layout

```
tests/
├── __init__.py
├── conftest.py            # Shared fixtures (tmp_path, cli_runner)
├── unit/
│   └── __init__.py
│   └── test_scaffold.py   # Unit tests for scaffolding logic
│   └── test_checks.py     # Unit tests for individual checks
├── integration/
│   └── __init__.py
│   └── test_init.py       # Integration tests for ase init
│   └── test_check.py      # Integration tests for ase check
└── test_main.py           # Smoke/sanity tests
```

---

## CI Wiring

GitHub Actions runs on push and PR:

```yaml
test:
  steps:
    - run: uv sync --group dev
    - run: uv run pytest
```

Pytest configuration in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

No traceability enforcement in CI yet — that arrives in Phase G.

---

## Maturity

| Layer | Maturity |
|---|---|
| L1 Unit | Documented, not yet CI-enforced |
| L3 Integration | Documented, not yet CI-enforced |
| AC traceability | Documented — Phase G target |
| AC fidelity check | Target state — Phase H target |

---

*Instantiates `docs/testing-convention.md`. Update this file when adding new test infrastructure, CI gates, or capability prefixes.*
