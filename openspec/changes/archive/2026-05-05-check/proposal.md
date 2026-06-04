# Proposal: Deterministic Check Framework

## Why

`iec init` can scaffold the canonical directory structure, but the tool has no way to validate whether a repo actually follows Intent Engineering practices. Every check in the plan (AGENTS.md exists, ADRs follow MADR, specs have AC IDs, tests trace to ACs) needs a shared mechanism to discover, register, run, and report. Without a framework, each check would duplicate discovery logic, result formatting, and CLI wiring.

## What Changes

- **Plugin registry**: Checkers are discovered and registered via a central registry. New checkers are added by creating a module — no CLI wiring changes needed.
- **Checker interface (Protocol)**: Every checker implements a lightweight protocol: one method that takes a repo path returns a result. No base class required.
- **Shared result model**: Structured result type (pass / warn / fail), severity, message, optional location (file path, line), and traceability (AC ID reference).
- **`iec check` command**: CLI entry point that runs registered checkers, collects results, and prints a summary. Accepts `--path` to scope to a directory or file. `--all` flag reserved for future agent-assisted checks.
- **No spec modifications**: Both existing capabilities (`scaffold-command`, `vendor-generators`) are unchanged.

## Capabilities

### New Capabilities

- `checker-registry`: Discovery, registration, and execution of checker plugins. Each checker has a unique ID, optional dependencies, and a run method.
- `check-result-model`: Structured result type with pass/warn/fail status, severity, message, optional source location, and AC ID for traceability.
- `check-cli`: The `iec check` command — runs registered checkers, outputs human-readable summary, exits with appropriate code (0 = all pass, 1 = warnings, 2 = failures).

### Modified Capabilities

*(None — all existing specs unchanged)*

## Impact

- **New module**: `src/iec_cli/check.py` — CLI command, registry, result model, and checker protocol (~200 lines)
- **`src/iec_cli/main.py`**: Wire `check` command (one import, one `app.add_typer()` call)
- **`pyproject.toml`**: New pytest markers as needed
- **No dependencies**: Pure Python, no external libraries beyond existing Typer
- **No breaking changes**: `iec init` is unaffected
