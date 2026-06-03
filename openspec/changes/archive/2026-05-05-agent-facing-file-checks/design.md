# Design: Agent-Facing File Checks

## Context

The check framework from Change 002 provides a `Registry`, `Checker` protocol, and `CheckResult` model. Now the first real checkers are needed. These three validate the most critical agent-facing file: `AGENTS.md`. They are the first consumers of the framework and will establish patterns for all future checkers.

## Goals / Non-Goals

**Goals:**
- `agents-exists`: Verify `AGENTS.md` is present at repo root
- `agents-size`: Verify `AGENTS.md` is under a configurable line limit (env var `ASE_AGENTS_MAX_LINES`, default 50)
- `agents-links`: Verify every Markdown link in `AGENTS.md` has descriptive text — no bare URLs
- Each checker is a class + `@registry.register`, lives in `src/ase_cli/checkers/`
- `_load_checkers()` in `check.py` imports the checkers package so checkers self-register
- Plain text output — match existing `ase check` style

**Non-Goals:**
- Config file support (`.ase.toml`) — env vars only for now
- HTML/multi-line link parsing — standard Markdown inline links only
- Auto-fix mode — detection only, no modification of AGENTS.md
- Deep link validation (broken links, 404s) — content-level only

## Decisions

### Decision 1: Package `src/ase_cli/checkers/` over flat modules

**Chosen**: `src/ase_cli/checkers/` package with `__init__.py`, `agents_exists.py`, `agents_size.py`, `agents_links.py`.

**Alternatives considered**:
- Flat files in `src/ase_cli/`: Clutters the source root as checker count grows (14+ planned).
- Single file: One 300+ line file with all checkers. Harder to navigate.

**Rationale**: A dedicated package keeps checkers isolated, discoverable, and easy to test. `__init__.py` imports all modules so `_load_checkers()` just does `import ase_cli.checkers`.

### Decision 2: Environment variable for agents-size limit

**Chosen**: `ASE_AGENTS_MAX_LINES` env var with default 50.

**Alternatives considered**:
- Hardcoded constant: No configurability.
- `.ase.toml` config file: Premature. No config file system exists yet.
- CLI flag: `ase check --max-lines 50`. Clutters the check command with checker-specific flags.

**Rationale**: Env vars are zero-cost, universally understood, and easy to set in CI. When a config file system is introduced (post v0.7.0), env vars can be promoted to file entries without breaking.

### Decision 3: Lines counted as `\n`-delimited, blank lines included

**Chosen**: Count every line in the file, including blank lines and frontmatter.

**Rationale**: Simple, unambiguous. "Under 50 lines" means exactly what the reader expects. Excluding blank lines would make the check unpredictable.

### Decision 4: Link description detection via regex + line context

**Chosen**: Parse Markdown inline links `[text](url)` and check if the containing line has substantive text after the link. A "bare link" is a list item where the link is the only substantive content — no trailing description.

**Alternatives considered**:
- Markdown parser libraries: Add a dependency for a simple check. Overkill.
- Check if the text inside brackets differs from the URL: Too narrow — `[AGENTS.md](AGENTS.md)` is still a bare link if no description follows.

**Rationale**: Regex is sufficient for standard AGENTS.md links. The check looks for list items (`- [...]`) where the line ends immediately after the link, or where the same list item has a bare URL with no dash-separated description.

### Decision 5: WARN severity for bare links, not FAIL

**Chosen**: `Severity.MEDIUM` with `Status.WARN` for bare links.

**Rationale**: A bare link is a quality issue, not a missing file. `agents-exists` is a hard FAIL — no AGENTS.md means the agent is blind. A bare link means the agent might load unnecessary context. Severity reflects the difference.

## Risks / Trade-offs

- **[Risk]** Regex-based link detection misses edge cases (nested brackets, escaped parens)
  → **Mitigation**: AGENTS.md links are simple — `[text](path.md) — description`. Standard patterns cover 99% of cases. Edge cases can be addressed in bug-fix releases.

- **[Risk]** `ASE_AGENTS_MAX_LINES` env var is not discoverable
  → **Mitigation**: Document in check output message: "AGENTS.md has 72 lines (limit: 50). Set ASE_AGENTS_MAX_LINES to change limit."

- **[Trade-off]** No `--fix` mode for bare links
  → Accept. Detection-first approach. coding agents can write descriptions themselves — the check flags what needs attention.
