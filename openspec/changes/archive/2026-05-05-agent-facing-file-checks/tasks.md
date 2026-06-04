# Tasks: Agent-Facing File Checks

## 1. Checkers package setup

- [x] 1.1 Create `src/iec_cli/checkers/` package with `__init__.py` that imports all checker modules

## 2. agents-exists — implementation and proof

- [x] 2.1 Create `src/iec_cli/checkers/agents_exists.py` with `AgentsExists` checker class, decorated with `@registry.register`
- [x] 2.2 Positive + negative unit tests: AGENTS.md found returns PASS, AGENTS.md missing returns FAIL, checker self-registers [AGEX-001, AGEX-002, AGEX-003]

## 3. agents-size — implementation and proof

- [x] 3.1 Create `src/iec_cli/checkers/agents_size.py` with `AgentsSize` checker class, reading `ASE_AGENTS_MAX_LINES` env var (default 50)
- [x] 3.2 Positive + negative unit tests: under limit returns PASS, exceeds limit returns FAIL, env var overrides default, missing file returns FAIL, invalid env var falls back to default [AGSZ-001, AGSZ-002, AGSZ-003, AGSZ-004, AGSZ-005]
- [x] 3.3 Unit test: checker self-registers [AGSZ-006]

## 4. agents-links — implementation and proof

- [x] 4.1 Create `src/iec_cli/checkers/agents_links.py` with `AgentsLinks` checker class, parsing `[text](url)` links and detecting bare links
- [x] 4.2 Positive + negative unit tests: all links described returns PASS, bare link returns WARN, multiple bare links all reported, missing file returns FAIL [AGLN-001, AGLN-002, AGLN-003, AGLN-005]
- [x] 4.3 Unit test: checker self-registers [AGLN-006]

## 5. Wiring — _load_checkers and CLI integration

- [x] 5.1 Implement `_load_checkers()` in `src/iec_cli/check.py` to import `iec_cli.checkers` package
- [x] 5.2 Integration test: `iec check` runs all three checkers against iec-cli's own repo [AGEX-001, AGSZ-001, AGLN-001]
- [x] 5.3 Integration test: `iec check` reports FAIL when AGENTS.md is missing in an empty directory [AGEX-002, AGSZ-004, AGLN-005]

## 6. Verify

- [x] 6.1 Run `uv run ruff check` — no lint errors
- [x] 6.2 Run `uv run ruff format --check` — no formatting issues
- [x] 6.3 Run `uv run pytest -v` — all 15 AC IDs proven (AGEX 3, AGSZ 6, AGLN 6)
