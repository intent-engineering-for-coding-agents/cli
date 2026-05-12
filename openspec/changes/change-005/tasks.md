# Tasks: ADR Format Checks

## 1. Test fixtures

- [x] 1.1 Create `tests/fixtures/adr/valid_bullet.md` — complete, valid bullet-style ADR (`* Status: accepted`, `## Context and Problem Statement`, `## Decision Outcome`, numbered title)
- [x] 1.2 Create `tests/fixtures/adr/valid_yaml.md` — complete, valid YAML front matter ADR (`status: accepted` in front matter, plain title, same required sections)
- [x] 1.3 Create `tests/fixtures/adr/missing_title.md` — no `#` heading
- [x] 1.4 Create `tests/fixtures/adr/title_mismatch.md` — `# ADR-0002: Wrong` heading (to be placed as `0001-*.md` in tests)
- [x] 1.5 Create `tests/fixtures/adr/missing_context.md` — missing `## Context and Problem Statement`
- [x] 1.6 Create `tests/fixtures/adr/missing_decision.md` — missing `## Decision Outcome`
- [x] 1.7 Create `tests/fixtures/adr/missing_status.md` — no `* Status:` and no YAML `status:` field
- [x] 1.8 Create `tests/fixtures/adr/invalid_status_bullet.md` — `* Status: draft`
- [x] 1.9 Create `tests/fixtures/adr/invalid_status_yaml.md` — `status: draft` in YAML front matter
- [x] 1.10 Create `tests/fixtures/adr/superseded_bullet.md` — `* Status: superseded by [ADR-0003](0003-title.md)` (valid superseded with reference)

## 2. adr-format — implementation and proof

- [x] 2.1 Create `src/ase_cli/checkers/adr_format.py` — walks `docs/decisions/`, skips `README.md` and `INDEX.md`, validates: filename pattern, `#` title heading (numbered prefix match only when `# ADR-NNNN:` style), `## Context and Problem Statement`, `## Decision Outcome`, status in bullet or YAML front matter format
- [x] 2.2 Positive tests using fixtures: valid bullet ADR passes all checks [ADRF-001, ADRF-007], valid YAML ADR passes all checks [ADRF-012, ADRF-013], plain title accepted [ADRF-012], superseded-with-reference passes [ADRF-015]
- [x] 2.3 Negative tests using fixtures: invalid filename [ADRF-002], no title heading [ADRF-003], numbered title mismatch [ADRF-004], missing Context section [ADRF-005], missing Decision Outcome section [ADRF-006], no status anywhere [ADRF-008], invalid bullet status [ADRF-009], invalid YAML status [ADRF-014]
- [x] 2.4 Boundary tests: `docs/decisions/` absent or empty returns PASS [ADRF-010], checker self-registers [ADRF-011]

## 3. adr-index — implementation and proof

- [x] 3.1 Create `src/ase_cli/checkers/adr_index.py` — verifies `docs/decisions/README.md` exists (when ADR files are present) and contains a Markdown link for every `NNNN-*.md` file in the directory
- [x] 3.2 Positive unit tests: README.md exists with all ADRs linked [ADRI-001, ADRI-004]
- [x] 3.3 Negative unit tests: README.md missing when ADRs exist [ADRI-002], `docs/decisions/` absent or empty returns PASS [ADRI-003], one ADR unlisted [ADRI-005], multiple ADRs unlisted [ADRI-006]
- [x] 3.4 Registration test: checker self-registers [ADRI-007]

## 4. Migrate ase-cli ADRs to YAML front matter

- [x] 4.1 Convert `docs/decisions/0001-python-typer.md` to YAML front matter
- [x] 4.2 Convert `docs/decisions/0002-canonical-docs-dir.md` to YAML front matter
- [x] 4.3 Convert `docs/decisions/0003-two-layer-checks.md` to YAML front matter
- [x] 4.4 Convert `docs/decisions/0004-byok-mcp.md` to YAML front matter
- [x] 4.5 Convert `docs/decisions/0005-madr-format.md` to YAML front matter
- [x] 4.6 Convert `docs/decisions/0006-openspec.md` to YAML front matter

## 5. Wiring

- [x] 5.1 Update `src/ase_cli/checkers/__init__.py` to import `adr_format` and `adr_index`
- [x] 5.2 Integration test: `ase check` runs all checkers against ase-cli's own repo and both new checkers pass on the migrated `docs/decisions/`

## 6. Verify

- [x] 6.1 Run `uv run ruff check` — no lint errors
- [x] 6.2 Run `uv run ruff format --check` — no formatting issues
- [x] 6.3 Run `uv run pytest -v` — all 22 AC IDs proven (ADRF 15, ADRI 7)
