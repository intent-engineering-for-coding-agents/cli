## Why

Adopting ASE practices currently requires manually creating the canonical directory structure — `docs/`, `openspec/`, `.agents/`, `AGENTS.md` — and remembering every subdirectory, every README stub, every convention. That's tedious, error-prone, and a barrier to adoption. `ase init` automates the bootstrap so any repo can adopt ASE conventions in a single command.

## What Changes

- **New command `ase init`** — scaffolds the canonical ASE directory structure in the current repo (or a specified path). Creates empty directories, stub files (AGENTS.md, README.md, INDEX.md, testing-convention.md, testing-strategy.md stub), and an AGENTS.md skeleton.
- **New flag `--with-claude`** — emits `CLAUDE.md` containing `@AGENTS.md` import syntax (Claude Code does not auto-discover `AGENTS.md`; it needs an explicit import in its native `CLAUDE.md` format).
- **New flag `--with-gemini`** — emits `.gemini/settings.json` configured to read `AGENTS.md` as context (Gemini CLI does not auto-discover `AGENTS.md` either).
- **Dry-run mode** (`--dry-run`) — prints what would be created without touching the filesystem.
- **Idempotent** — running `ase init` on an already-initialized repo is safe; existing files are never overwritten unless `--force` is passed.

## Capabilities

### New Capabilities

- `scaffold-command`: The `ase init` subcommand that creates the canonical ASE directory structure (`docs/`, `openspec/`, `.agents/`, `AGENTS.md` skeleton) in a target repository. Supports dry-run, force overwrite, and path targeting.
- `vendor-generators`: Emit vendor-specific agent instruction pointer files for the two tools that do NOT auto-discover `AGENTS.md`: **Claude Code** (`CLAUDE.md` via `--with-claude`, using `@AGENTS.md` import) and **Gemini CLI** (`.gemini/settings.json` via `--with-gemini`). All other major tools (Codex, Copilot, Cursor, Windsurf, Devin, Aider, Zed, etc. — 20+ tools) read `AGENTS.md` natively and need no pointer file.

### Modified Capabilities

<!-- None — this is the first feature built on top of the scaffolded project. -->

## Impact

- New CLI entry point: `ase init` subcommand added to `ase_cli.main` via Typer
- New source module: `src/ase_cli/init.py` (or `src/ase_cli/commands/init.py`)
- Directory scaffolding utilities: creating dirs, writing stub files
- `docs/testing-convention.md` ships as full static content (generic ASE testing conventions)
- `docs/testing-strategy.md` ships as a stub for project-specific instantiation
- Tests: new directory creation, idempotent re-run, dry-run output, vendor flag behavior
