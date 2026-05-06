# Tasks: Architecture & File Structure Checks

## 1. docs-readme-exists — implementation and proof

- [x] 1.1 Create `src/ase_cli/checkers/docs_readme_exists.py` with checker that walks `docs/` recursively, checks every subdirectory for `README.md`
- [x] 1.2 Positive + negative unit tests: all directories have README (positive), one missing (negative), multiple missing (negative), docs/ missing entirely (negative), checker self-registers [DRME-001, DRME-002, DRME-003, DRME-004, DRME-005]

## 2. docs-index-exists — implementation and proof

- [x] 2.1 Create `src/ase_cli/checkers/docs_index_exists.py` with checker that walks `docs/` recursively, checks every subdirectory for `INDEX.md`
- [x] 2.2 Positive + negative unit tests: all directories have INDEX (positive), one missing (negative), multiple missing (negative), docs/ missing entirely (negative), checker self-registers [DINE-001, DINE-002, DINE-003, DINE-004, DINE-005]

## 3. docs-index-stale — implementation and proof

- [x] 3.1 Create `src/ase_cli/checkers/docs_index_stale.py` with checker that walks `docs/`, finds every `INDEX.md`, parses links, cross-references against directory contents
- [x] 3.2 Positive + negative unit tests: all indices match (positive), broken link in one INDEX (negative), orphan file (negative), both broken + orphan across multiple INDEX files (negative), .gitkeep excluded (boundary), docs/ missing entirely (negative) [DINS-001, DINS-002, DINS-003, DINS-004, DINS-005, DINS-006]
- [x] 3.3 Unit test: checker self-registers [DINS-007]

## 4. Wiring

- [x] 4.1 Update `src/ase_cli/checkers/__init__.py` to import new checker modules
- [x] 4.2 Integration test: `ase check` runs all six checkers against ase-cli's own repo

## 5. Verify

- [x] 5.1 Run `uv run ruff check` — no lint errors
- [x] 5.2 Run `uv run ruff format --check` — no formatting issues
- [x] 5.3 Run `uv run pytest -v` — all 17 AC IDs proven (DRME 5, DINE 5, DINS 7)
