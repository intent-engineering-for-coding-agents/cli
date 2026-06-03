# Design: Deterministic Check Framework

## Context

`ase init` scaffolds the canonical directory structure. Now the tool needs to validate ASE practices in any repo. The plan defines 14+ checkers across Changes 003–010. Without a shared framework, each checker would duplicate discovery logic, result formatting, and CLI wiring.

This design covers the architectural backbone — registry, protocol, result model, and CLI command. Individual checker implementations are out of scope.

## Goals / Non-Goals

**Goals:**
- Single-module framework: `src/ase_cli/check.py` (~200 lines)
- Decorator-based checker registration (zero-config, discoverable)
- Structured result model with pass/warn/fail, severity, and AC traceability
- `ase check` CLI command: runs registered checkers, prints summary, exits with appropriate code
- Open for extension: adding a checker = create a class/decorated function + import it

**Non-Goals:**
- Individual checker implementations (`agents-exists`, `adr-format`, etc.)
- agent-assisted checks (MCP server, Change 011)
- `--all` flag wiring (reserved, not implemented)
- Third-party plugin system (entry_points, namespace packages)
- Config file support (.ase.toml)
- JSON/machine-readable output format

## Decisions

### Decision 1: Protocol over ABC

**Chosen**: `typing.Protocol` for the checker interface.

**Alternatives considered**:
- `abc.ABC`: Requires explicit inheritance. More ceremony, less flexible.
- Callable protocol: A function `(Path) -> CheckResult`. Clean but limits metadata (ID, description).

**Rationale**: Protocol enables structural subtyping — any class with a `check(path: Path) -> CheckResult` method is a checker, no inheritance needed. This matches how pytest fixtures and hooks work. Each checker is a class with `.id`, `.description`, and `.check()` — lightweight, self-documenting.

### Decision 2: Decorator-based registry

**Chosen**: `@registry.register` decorator on checker classes.

**Alternatives considered**:
- Explicit import list: `CHECKERS = [AgentsExists(), ...]`. Simple but requires updating a central file for each new checker. Error-prone.
- Module auto-discovery (`importlib.import_module` on a `checkers/` directory): Premature for first-party checkers. Adds complexity without benefit.
- Setuptools entry_points: Overkill. These are internal checkers, not third-party plugins.

**Rationale**: A decorator is the Pythonic standard for plugin registration (see pytest markers, Flask routes, Typer commands). Each checker file imports the registry and decorates its class. `ase check` calls `registry.run_all(path)` — it doesn't know or care about individual checker modules.

### Decision 3: Single module file, not package

**Chosen**: `src/ase_cli/check.py` as a single module.

**Alternatives considered**:
- Package (`src/ase_cli/check/` with `__init__.py`, `registry.py`, `result.py`, `cli.py`): Better for large check frameworks. Premature for 200 lines.

**Rationale**: Start with one file. If Type 003–005 checkers push it past ~400 lines, extract a package. The module boundary is clear — `from ase_cli.check import registry, CheckResult` works either way. Change 002's `check.py` can become `check/__init__.py` later without breaking imports.

### Decision 4: Result model as dataclass

**Chosen**: `@dataclass` for `CheckResult`. `@unique Enum` for `Status` and `Severity`.

**Rationale**: Standard Python, no external dependencies. Dataclass gives free `__eq__`, `__repr__`, and `__init__`. Enums prevent typos in status values. The result model is simple enough that Pydantic would be overkill.

### Decision 5: ASCII-only CLI output

**Chosen**: Plain text output with indentation, no color codes.

**Alternatives considered**:
- Rich library: Beautiful but adds a dependency. Revisit when user experience matters more.
- No output format yet: Users need to see results. Plain text is zero-cost and works everywhere.

**Rationale**: Match the existing `ase init` style — clean, minimal output. Color and formatting can be added later as non-breaking enhancements.

## Data Model

```
Status = PASS | WARN | FAIL
Severity = HIGH | MEDIUM | LOW

CheckResult:
    check_id: str          # e.g. "agents-exists"
    status: Status
    message: str           # Human-readable explanation
    severity: Severity     # Default HIGH for FAIL, MEDIUM for WARN
    location: str | None   # e.g. "AGENTS.md:42" or "docs/"
    ac_id: str | None      # e.g. "CHKREG-003" for traceability

Checker (Protocol):
    id: str                # Unique check identifier
    description: str       # One-line what this check validates
    check(path: Path) -> CheckResult

Registry:
    register(checker: Checker) -> None
    run_all(path: Path) -> list[CheckResult]
    run_one(check_id: str, path: Path) -> CheckResult
```

## Architecture

```
ase check [--path <dir>]
    │
    ▼
main.py: app.add_typer(check_app)
    │
    ▼
check.py: check_app (Typer)
    │
    ├── registry.run_all(Path) → list[CheckResult]
    │       │
    │       └── for each registered Checker:
    │               checker.check(path)
    │
    ├── ResultCollector aggregates results
    │       ├── pass_count, warn_count, fail_count
    │       └── by_severity, by_checker groupings
    │
    └── Output formatter prints summary
            ├── Per-checker: ✓ PASS / ⚠ WARN / ✗ FAIL
            └── Exit code: 0 (all pass), 1 (warnings), 2 (failures)
```

## Risks / Trade-offs

- **[Risk]** Single-file module grows beyond maintainable size in Change 003–005
  → **Mitigation**: Extract to `src/ase_cli/check/` package when `check.py` exceeds 400 lines. Protocol and result model are import-stable (`from ase_cli.check import ...`).

- **[Risk]** Decorator registration means checker modules must be imported somewhere before `run_all()` is called
  → **Mitigation**: `check.py` explicitly imports all checker modules in a `_load_checkers()` function called once at startup. This is intentional — no magic, no auto-discovery of unexpected modules.

- **[Risk]** No check ordering or dependency mechanism yet
  → **Mitigation**: Accept for now. Checkers run in registration order. If ordering becomes important (e.g., `agents-exists` must run before `agents-size`), add a `depends_on: list[str]` field to the protocol. Non-breaking addition.

- **[Trade-off]** No `--format json` yet
  → Accept. Machine-readable output is useful for CI but adds complexity. Plain text is sufficient for human users in v0.3.0. JSON output can be added as a non-breaking extension.
