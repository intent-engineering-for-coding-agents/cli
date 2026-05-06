# Design: Architecture & File Structure Checks

## Context

Change 003 checks `AGENTS.md`. Now we extend to the `docs/` directory tree. ASE conventions require every `docs/` subdirectory to have both `README.md` and `INDEX.md`. Both serve as entry points but for different audiences — README for humans (renders on GitHub), INDEX for agents (loaded first for context economy).

## Goals / Non-Goals

**Goals:**
- `docs-readme-exists`: Walk `docs/` recursively, report any subdirectory missing `README.md`
- `docs-index-exists`: Walk `docs/` recursively, report any subdirectory missing `INDEX.md` as WARN (not FAIL — context economy is an optimization)
- `docs-index-stale`: For each INDEX.md, parse Markdown links, compare against files in that same directory, report broken links and orphans
- `.gitkeep` excluded from orphan detection
- Follow same checker pattern: class + `@registry.register`, single module per checker

**Non-Goals:**
- Checking directories outside `docs/`
- Deep content validation of README or INDEX
- Cross-directory link checking (only within each INDEX's own directory)

## Decisions

### Decision 1: Recursive directory walk with `os.walk` equivalent

**Chosen**: `path.rglob("*")` or manual recursion. For each directory under `docs/`, check for README.md and INDEX.md. Root `docs/` itself is included.

**Rationale**: Simple, standard. Directories without any files (only `.gitkeep`) are still expected to have README.md and INDEX.md.

### Decision 2: INDEX.md parsing per-directory

**Chosen**: For each `INDEX.md`, parse lines with Markdown links `[text](path)`. Treat paths as relative to that INDEX.md's directory (not `docs/` root). Compare against `listdir()` of that same directory.

**Rationale**: Each INDEX.md describes its own directory. Using relative paths is simpler and more intuitive than tracking full `docs/`-relative paths.

### Decision 3: WARN for stale, FAIL for missing

**Chosen**: Stale index issues = WARN (`Severity.MEDIUM`). Missing README = FAIL (`Severity.HIGH`). Missing INDEX = WARN (`Severity.MEDIUM` — INDEX.md is context economy optimization, README.md is the canonical architecture overview).

**Rationale**: Missing files block agent boot. Stale entries waste context but don't break functionality.

### Decision 4: Report all issues in one result per checker

**Chosen**: Each checker returns a single `CheckResult`. README/INDEX checkers list all directories missing the file. Stale checker lists all broken links + orphans.

**Rationale**: One result per checker keeps output readable. A missing README in 5 directories is one FAIL listing all 5, not 5 separate check results.

## Risks / Trade-offs

- **[Trade-off]** No cross-directory link validation
  → Accept. INDEX.md files are directory-local by convention. Cross-directory validation would require understanding project structure.
