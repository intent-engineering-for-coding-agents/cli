## 1. Module setup

- [ ] 1.1 Create `src/ase_cli/init.py` with Typer app and `init` command placeholder
- [ ] 1.2 Wire `init` command into `src/ase_cli/main.py` (`app.add_typer(init_app, ...)`)

## 2. Directory scaffolding

- [ ] 2.1 Define `ASE_DIRS` constant with all canonical directory paths
- [ ] 2.2 Implement `scaffold_dirs(target: Path)` — creates all directories (respects `--force`)
- [ ] 2.3 Implement `scaffold_files(target: Path, force: bool)` — creates stub files (AGENTS.md, docs/README.md, docs/INDEX.md, docs/testing-convention.md, docs/testing-strategy.md, docs/decisions/README.md, docs/design/README.md)
- [ ] 2.4 Implement idempotency check — skip existing dirs/files unless `--force`

## 3. CLI flags

- [ ] 3.1 Implement `--path` flag (resolves relative/absolute, creates target dir if missing)
- [ ] 3.2 Implement `--dry-run` flag (logs what would happen, no filesystem writes)
- [ ] 3.3 Implement `--force` flag (overwrites existing files)

## 4. AGENTS.md skeleton

- [ ] 4.1 Define AGENTS.md template with TOC pattern (project header, instructions links, docs/INDEX.md reference)
- [ ] 4.2 Inject project name from target directory name as default placeholder

## 5. Testing convention scaffolding

- [ ] 5.1 Embed `docs/testing-convention.md` as static content (full ASE testing convention — test layers, AC IDs, traceability markers, proof requirements)
- [ ] 5.2 Create `docs/testing-strategy.md` stub referencing `testing-convention.md` with placeholder sections for test tools, CI wiring, and directory layout

## 6. Vendor generators

- [ ] 6.1 Implement `--with-claude` — creates `CLAUDE.md` with `@AGENTS.md` content
- [ ] 6.2 Implement `--with-gemini` — creates `.gemini/settings.json` with AGENTS.md context config
- [ ] 6.3 Vendor files respect `--dry-run` and `--force` like core scaffold files

## 7. Output and logging

- [ ] 7.1 Report created directories and files (list format, one per line)
- [ ] 7.2 Report skipped items (already exists)
- [ ] 7.3 Report "already initialized" when no work was done

## 8. Tests

- [ ] 8.1 Test `ase init` in empty directory — all dirs and files created
  - Covers: SCAFFOLD-001
- [ ] 8.2 Test `ase init` in partially initialized directory — missing items created, existing preserved
  - Covers: SCAFFOLD-002
- [ ] 8.3 Test `ase init` in fully initialized directory — nothing created, "already initialized" message
  - Covers: SCAFFOLD-003
- [ ] 8.4 Test AGENTS.md content — TOC pattern, project placeholder, INDEX.md link, under 25 lines
  - Covers: SCAFFOLD-004
- [ ] 8.5 Test `ase init --dry-run` — no filesystem changes, correct output listing
  - Covers: SCAFFOLD-005, SCAFFOLD-006
- [ ] 8.6 Test `ase init --force` — overwrites existing files
  - Covers: SCAFFOLD-007, SCAFFOLD-008
- [ ] 8.7 Test `ase init --path /tmp/some-target` — creates structure in target dir
  - Covers: SCAFFOLD-009, SCAFFOLD-010, SCAFFOLD-011
- [ ] 8.8 Test `ase init --with-claude` — `CLAUDE.md` created with `@AGENTS.md`
  - Covers: VENDOR-001, VENDOR-002, VENDOR-003, VENDOR-004
- [ ] 8.9 Test `ase init --with-gemini` — `.gemini/settings.json` created with correct JSON
  - Covers: VENDOR-005, VENDOR-006
- [ ] 8.10 Test `ase init --with-claude --with-gemini` — both vendor files created
  - Covers: VENDOR-007
- [ ] 8.11 Test vendor flags with `--dry-run` — files listed but not created
  - Covers: VENDOR-008
- [ ] 8.12 Test vendor flags with `--force` — overwrites existing vendor files
  - Covers: VENDOR-003
- [ ] 8.13 Test `docs/testing-convention.md` content — contains test layer taxonomy, AC ID format, traceability conventions
  - Covers: SCAFFOLD-012
- [ ] 8.14 Test `docs/testing-strategy.md` stub — references convention, has placeholder sections
  - Covers: SCAFFOLD-013

## 9. Verify

- [ ] 9.1 Run `ruff check` and `ruff format` — no errors
- [ ] 9.2 Run `pytest` — all tests pass
- [ ] 9.3 Run `ase init` on ase-cli itself with `--dry-run` — verify idempotency report
- [ ] 9.4 Verify all 21 AC IDs are covered by test tasks (SCAFFOLD-001..013, VENDOR-001..008)
