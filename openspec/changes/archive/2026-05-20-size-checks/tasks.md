# Tasks: File and Spec Size Checks

## 1. spec-size — implementation and proof

- [x] 1.1 Create `src/ase_cli/checkers/spec_size.py` — `SpecSize` class, uses `find_spec_files`, counts lines per file, returns WARN if over configurable limit (env `ASE_SPEC_MAX_LINES`, default 500)
- [x] 1.2 Positive tests: no spec files returns PASS [SPSZ-004], under limit returns PASS [SPSZ-001]
- [x] 1.3 Negative tests: over limit returns WARN with line count in message [SPSZ-002], env override tightens limit and triggers WARN [SPSZ-003]
- [x] 1.4 Edge case: invalid env var falls back to default 500 [SPSZ-005]
- [x] 1.5 Registration test [SPSZ-006]

## 2. file-size — implementation and proof

- [x] 2.1 Create `src/ase_cli/checkers/file_size.py` — `FileSize` class, walks `*.md` skipping `.git/node_modules/.venv/.vitepress/__pycache__`, counts lines, returns WARN if over limit (env `ASE_FILE_MAX_LINES`, default 500)
- [x] 2.2 Positive tests: no .md files returns PASS [FLSZ-004], under limit returns PASS [FLSZ-001]
- [x] 2.3 Negative tests: over limit returns WARN with line count [FLSZ-002], env override tightens limit [FLSZ-003]
- [x] 2.4 Boundary: file inside node_modules/ not counted [FLSZ-005]
- [x] 2.5 Edge case: invalid env var falls back to default [FLSZ-006]
- [x] 2.6 Registration test [FLSZ-007]

## 3. Wiring

- [x] 3.1 Update `src/ase_cli/checkers/__init__.py` to import `spec_size`, `file_size`
- [x] 3.2 Update integration test to register and assert new checkers appear in output

## 4. Verify

- [x] 4.1 Run `uv run ruff check` — no lint errors
- [x] 4.2 Run `uv run ruff format --check` — no formatting issues
- [x] 4.3 Run `uv run pytest -v` — all 13 AC IDs proven (SPSZ-001..006, FLSZ-001..007)
