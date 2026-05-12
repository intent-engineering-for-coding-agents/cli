# Tasks: docs-index-scope

## 1. Shared link parser

- [x] 1.1 Add `LINK_RE` to `src/ase_cli/checkers/_shared.py` (promoted from `docs_index_stale.py`).
- [x] 1.2 Update `src/ase_cli/checkers/docs_index_stale.py` to import `LINK_RE` from `_shared`; remove the local copy.

## 2. New checker

- [x] 2.1 Create `src/ase_cli/checkers/docs_index_scope.py` with `DocsIndexScope` class, `@registry.register`, and the in-scope rule (same-dir or immediate sub-INDEX/README pointer; anchor fragments allowed).
- [x] 2.2 Register the module in `src/ase_cli/checkers/__init__.py`.

## 3. Tests

- [x] 3.1 New scenarios in `tests/test_docs_checkers.py`:
  - [x] DISO-001: same-dir file link → PASS
  - [x] DISO-002: immediate `subdir/INDEX.md` pointer → PASS
  - [x] DISO-003: immediate `subdir/README.md` pointer → PASS
  - [x] DISO-004: deeper path → WARN
  - [x] DISO-005: parent path → WARN
  - [x] DISO-006: absolute URL → WARN
  - [x] DISO-007: dirs without INDEX.md are skipped → PASS
  - [x] DISO-008: checker registered

## 4. Spec

- [x] 4.1 Create `openspec/specs/docs-index-scope/spec.md` with all DISO-001..008 scenarios.

## 5. Verify

- [x] 5.1 `uv run ruff check` — no lint errors
- [x] 5.2 `uv run ruff format --check` — no formatting issues
- [x] 5.3 `uv run pytest -v` — all DISO scenarios + all existing tests pass
- [x] 5.4 `uv run ase check --path C:\Code\ase-book` — confirm the new checker fires WARN on the *pre-cleanup* book `docs/INDEX.md`
