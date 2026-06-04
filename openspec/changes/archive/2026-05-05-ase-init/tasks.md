## 1. Module setup and CLI basics

- [x] 1.1 Create `src/iec_cli/init.py` with Typer app and `init` command placeholder
- [x] 1.2 Wire `init` command into `src/iec_cli/main.py`
- [x] 1.3 Add `--version` flag to CLI callback (reads from `importlib.metadata`)
- [x] 1.4 Update `docs/README.md` with accurate command reference (`--help`, `--version`, init flags)

## 2. Directory scaffolding

- [x] 2.1 Define `ASE_DIRS` constant with all canonical directory paths
- [x] 2.2 Implement `scaffold_dirs()` — creates all directories and `.gitkeep` files
- [x] 2.3 Implement `scaffold_files()` — creates stub files (AGENTS.md, docs/README.md, docs/INDEX.md, docs/testing-convention.md, docs/testing-strategy.md, docs/decisions/README.md, docs/design/README.md)
- [x] 2.4 Implement idempotency check — skip existing dirs/files unless `--force`

## 3. CLI flags

- [x] 3.1 Implement `--path` flag (resolves relative/absolute, creates target dir if missing)
- [x] 3.2 Implement `--dry-run` flag (logs what would happen, no filesystem writes)
- [x] 3.3 Implement `--force` flag (overwrites existing files)

## 4. AGENTS.md skeleton

- [x] 4.1 Define AGENTS.md template with TOC pattern (project header, instructions links, docs/INDEX.md reference)
- [x] 4.2 Inject project name from target directory name as default placeholder

## 5. Testing convention scaffolding

- [x] 5.1 Embed `docs/testing-convention.md` as static content (full Intent Engineering testing convention — test layers, AC IDs, traceability markers, proof requirements)
- [x] 5.2 Create `docs/testing-strategy.md` stub referencing `testing-convention.md` with placeholder sections for test tools, CI wiring, and directory layout

## 6. Vendor generators

- [x] 6.1 Implement `--with-claude` — creates `CLAUDE.md` with `@AGENTS.md` content
- [x] 6.2 Implement `--with-gemini` — creates `.gemini/settings.json` with AGENTS.md context config
- [x] 6.3 Vendor files respect `--dry-run` and `--force` like core scaffold files

## 7. Output and logging

- [x] 7.1 Report created directories and files (list format, one per line)
- [x] 7.2 Report skipped items (already exists)
- [x] 7.3 Report "already initialized" when no work was done

## 8. Test infrastructure

- [x] 8.1 Register pytest markers (`ac`, `baseline`, `sanity`) in `pyproject.toml`

## 9. Tests

- [x] 9.1 Test `iec init` in empty directory — all dirs and files created
  - Covers: SCAFFOLD-001
- [x] 9.2 Test `iec init` in partially initialized directory — missing items created, existing preserved
  - Covers: SCAFFOLD-002
- [x] 9.3 Test `iec init` in fully initialized directory — nothing created, "already initialized" message
  - Covers: SCAFFOLD-003
- [x] 9.4 Test AGENTS.md content — TOC pattern, project placeholder, INDEX.md link, under 25 lines
  - Covers: SCAFFOLD-004
- [x] 9.5 Test `iec init --dry-run` — no filesystem changes, correct output listing
  - Covers: SCAFFOLD-005, SCAFFOLD-006
- [x] 9.6 Test `iec init --force` — overwrites existing files
  - Covers: SCAFFOLD-007, SCAFFOLD-008
- [x] 9.7 Test `iec init --path` — creates structure in target dir
  - Covers: SCAFFOLD-009, SCAFFOLD-010, SCAFFOLD-011
- [x] 9.8 Test `iec init --with-claude` — `CLAUDE.md` created with `@AGENTS.md`
  - Covers: VENDOR-001, VENDOR-002, VENDOR-003, VENDOR-004
- [x] 9.9 Test `iec init --with-gemini` — `.gemini/settings.json` created with correct JSON
  - Covers: VENDOR-005, VENDOR-006
- [x] 9.10 Test `iec init --with-claude --with-gemini` — both vendor files created
  - Covers: VENDOR-007
- [x] 9.11 Test vendor flags with `--dry-run` — files listed but not created
  - Covers: VENDOR-008
- [x] 9.12 Test vendor flags with `--force` — overwrites existing vendor files
  - Covers: VENDOR-003
- [x] 9.13 Test `docs/testing-convention.md` content — contains test layer taxonomy, AC ID format, traceability conventions
  - Covers: SCAFFOLD-012
- [x] 9.14 Test `docs/testing-strategy.md` stub — references convention, has placeholder sections
  - Covers: SCAFFOLD-013
- [x] 9.15 Test `.gitkeep` files in empty directories, absent where stubs exist
  - Covers: SCAFFOLD-014
- [x] 9.16 Test `iec --help` shows commands
  - Covers: SCAFFOLD-015
- [x] 9.17 Test `iec --version` shows version from pyproject.toml
  - Covers: SCAFFOLD-016

## 10. Verify

- [x] 10.1 Run `ruff check` and `ruff format` — no errors
- [x] 10.2 Run `pytest` — all tests pass (21 tests)
- [x] 10.3 Run `iec init` on iec-cli itself with `--dry-run` — verify idempotency report
- [x] 10.4 Verify all 24 AC IDs are covered (SCAFFOLD-001..016, VENDOR-001..008)
