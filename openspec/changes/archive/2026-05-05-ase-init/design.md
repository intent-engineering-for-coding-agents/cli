## Context

`iec-cli` is a Python CLI (Typer, Python 3.12+) currently at `v0.2.0` with the canonical directory structure, ADRs, AGENTS.md, and `.agents/` hub already in place. There is no command to scaffold this structure into another repo. The `iec init` command is the first user-facing feature and sets the foundation for all future checks (which depend on the directory structure being present).

## Goals / Non-Goals

**Goals:**
- `iec init` creates the full canonical Intent Engineering directory structure in any target directory
- Creates AGENTS.md skeleton, docs/README.md, docs/INDEX.md, docs/testing-convention.md, docs/testing-strategy.md stub, and subdirectory README stubs
- `--with-claude` emits `CLAUDE.md` with `@AGENTS.md` import
- `--with-gemini` emits `.gemini/settings.json` with AGENTS.md context path
- `--dry-run` previews what would be created without touching disk
- `--force` overwrites existing files (default: never overwrite)
- `--path` targets a specific directory (default: `.`)
- Idempotent: running twice does nothing (unless `--force`)

**Non-Goals:**
- No template customization (v1 emits fixed content)
- No interactive prompts during init
- No `iec generate` subcommand yet (Phase I, Change 012)
- No validation that the target directory is a git repo
- No removal/cleanup of previous Intent Engineering files

## Decisions

### 1: Single `init.py` module, no plugin architecture yet

The scaffolding logic is ~150 lines of directory creation + file writing. A single module at `src/iec_cli/init.py` is sufficient. The check framework (Change 002) will introduce the plugin architecture. No need to over-engineer here.

### 2: `--with-<vendor>` flags vs `--vendor claude,gemini`

Vendor flags are independent (you might want Claude only). Individual `--with-claude` / `--with-gemini` flags are more discoverable than `--vendor claude --vendor gemini`. Composable: `iec init --with-claude --with-gemini` works naturally.

### 3: Idempotency by file existence check

Each file/directory is checked with `os.path.exists()` before creation. If it exists and `--force` is not set, skip it with a log message. No checksum comparison — existence is the signal.

### 4: `CLAUDE.md` contains `@AGENTS.md` import, not "See AGENTS.md"

Claude Code supports `@AGENTS.md` as a native import directive. The emitted `CLAUDE.md` will be:
```
@AGENTS.md
```
This is minimal, works with Claude Code's hierarchical file loading, and avoids duplication.

### 5: `.gemini/settings.json` uses Gemini CLI's context file config

```json
{
  "context": {
    "fileName": "AGENTS.md"
  }
}
```

### 6: AGENTS.md skeleton uses the TOC pattern

The generated AGENTS.md follows the project's own pattern: short header with project name, language/framework, commands section, and links to loaded instructions. Under 20 lines — a TOC, not an encyclopedia.

## Risks / Trade-offs

- **[Risk] `--force` overwrites user-modified AGENTS.md** → Mitigation: `--force` is opt-in and documented with a warning
- **[Risk] Generated files get stale as Intent Engineering conventions evolve** → Mitigation: `iec check` will catch stale structure (Phase E); init is snapshot only
- **[Trade-off] No `iec generate` subcommand yet** → Later Phase I will add `iec generate copilot`/`claude`. For now, `--with-*` flags on `iec init` are sufficient as the bootstrap moment is when vendor files are most naturally created.

## Open Questions

- Should `iec init` also run `openspec init`? (Decided: no — OpenSpec has its own workflow. Intent Engineering and OpenSpec are complementary, not bundled.)
