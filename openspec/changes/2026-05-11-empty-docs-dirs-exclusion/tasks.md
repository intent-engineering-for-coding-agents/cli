# Tasks: Exempt effectively-empty docs/ subdirectories

## 1. Shared helper

- [x] 1.1 Create `src/ase_cli/checkers/_shared.py` with `is_effectively_empty(dirpath: Path) -> bool`. Recursive walk; ignore entries whose name starts with `.`.

## 2. docs-readme-exists — extend rule

- [x] 2.1 Update `src/ase_cli/checkers/docs_readme_exists.py` to skip effectively-empty subdirectories before recording a missing `README.md`.
- [x] 2.2 New scenarios in `tests/test_docs_checkers.py`:
  - [x] `.gitkeep`-only subdir → PASS [DRME-006]
  - [x] Dotfiles-only subdir → PASS [DRME-006]
  - [x] Nested empty subdir → PASS [DRME-006]
  - [x] `.gitkeep` plus real file → FAIL [DRME-006]
- [x] 2.3 Update existing DRME-002, DRME-003 fixtures to add a substantive file in the missing-README subdir (the scenarios are about a populated subdir lacking a README, not about an empty placeholder).

## 3. docs-index-exists — extend rule

- [x] 3.1 Update `src/ase_cli/checkers/docs_index_exists.py` with the symmetric change.
- [x] 3.2 New scenarios in `tests/test_docs_checkers.py`:
  - [x] `.gitkeep`-only subdir → PASS [DINE-006]
  - [x] Dotfiles-only subdir → PASS [DINE-006]
  - [x] Nested empty subdir → PASS [DINE-006]
  - [x] `.gitkeep` plus real file → WARN [DINE-006]
- [x] 3.3 Update existing DINE-002, DINE-003 fixtures to add a substantive file in the missing-INDEX subdir.

## 4. Specs

- [x] 4.1 Append `DRME-006` requirement + scenarios to `openspec/specs/docs-readme-exists/spec.md`.
- [x] 4.2 Append `DINE-006` requirement + scenarios to `openspec/specs/docs-index-exists/spec.md`.

## 5. Verify

- [ ] 5.1 `uv run ruff check` — no lint errors
- [ ] 5.2 `uv run ruff format --check` — no formatting issues
- [ ] 5.3 `uv run pytest -v` — all DRME, DINE scenarios green (including the four new ones per checker)
- [ ] 5.4 Reinstall `ase-cli` in the ase-book repo and confirm `ase check` returns all-PASS.
