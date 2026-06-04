# iec-cli Test Strategy

Authoritative reference for test types, frameworks, file locations, coverage
thresholds, and the pytest marker convention. See `docs/testing-convention.md`
for the generic Intent Engineering testing convention this instantiates.

---

## Test Types and Frameworks

| Type | pytest location | Framework | What it covers |
|---|---|---|---|
| `Unit` | `tests/test_*.py` | pytest + `tmp_path` | Checker logic, pure functions, no CLI invocation |
| `Integration` | `tests/integration/test_*.py` | pytest + `typer.testing.CliRunner` + `tmp_path` | Full command invocation, exit codes, filesystem |
| `Sanity` | `tests/test_main.py` | pytest | Package importable, Typer app exists |
| `Manual` | Spec only — no test file | N/A | Steps that require human judgment |

---

## File Layout

```
tests/
├── __init__.py
├── test_main.py               # Sanity tests
├── test_check.py              # Unit — check framework (Registry, CheckResult)
├── test_checkers.py           # Unit — agents-exists, agents-size, agents-links
├── test_adr_checkers.py       # Unit — adr-format, adr-index
├── test_docs_checkers.py      # Unit — docs-readme-exists, docs-index-*
├── test_hub_secrets_checkers.py # Unit — agents-hub-structure, secrets
├── test_size_checkers.py      # Unit — spec-size, file-size
├── test_spec_quality_checkers.py # Unit — spec-ac-ids, spec-test-category
├── test_traceability_checker.py  # Unit — test-traceability, test-coverage
├── test_lifecycle_checkers.py # Unit — tasks-complete, change-archived
├── test_eval.py               # Unit — eval check types, _load_tasks
├── ac-registry.md             # AC ID prefix → component mapping
├── scenario-template.md       # Canonical scenario format + complexity tiers
├── fixtures/                  # Shared test fixtures (ADR files, etc.)
└── integration/
    ├── test_init.py           # Integration — iec init, vendor flags
    ├── test_check.py          # Integration — iec check CLI
    ├── test_checkers.py       # Integration — all checkers registered + run
    └── test_eval.py           # Integration — iec eval CLI
```

---

## Pytest Markers

Registered in `pyproject.toml`:

| Marker | Applied to |
|---|---|
| `@pytest.mark.ac("PREFIX-NNN")` | Any test proving a specific AC |
| `@pytest.mark.unit` | Unit tests |
| `@pytest.mark.integration` | Integration tests |
| `@pytest.mark.sanity` | Sanity / toolchain tests |
| `@pytest.mark.baseline` | Coverage-threshold tests with no AC |

Multiple `@pytest.mark.ac()` decorators are allowed per test when one test proves
multiple ACs.

---

## Coverage Thresholds

| Tier | Positive tests | Negative tests | Rationale |
|---|---|---|---|
| Simple check (1 happy path) | 1 | 1 | Minimum viable proof |
| Medium check (2-3 paths) | 2-3 | 2 | Covers main variants + an edge |
| Complex check (many paths) | Several | Several | Determined per spec |

Every non-Manual AC must appear in at least one `@pytest.mark.ac()` decorator.
The `test-coverage` checker warns when fewer than 2 test files reference an AC.

---

## CI Gates

| Gate | Command | Added in |
|---|---|---|
| Lint | `uv run ruff check .` | Phase A |
| Format | `uv run ruff format --check .` | Phase A |
| Tests | `uv run pytest` | Phase A |
| Self-check | `uv run iec check` | Phase I |

The self-check step runs all 19 registered checkers against the iec-cli repo itself,
including `test-traceability` (AC markers) and `change-archived` (lifecycle gates).

---

*Supersedes the notes in `docs/testing-strategy.md`. Update this file when adding
new test infrastructure, CI gates, or capability prefixes.*
