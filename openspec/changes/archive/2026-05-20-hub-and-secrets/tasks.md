# Tasks: Agent Hub Structure and Secrets Checks

## 1. agents-hub-structure — implementation and proof

- [x] 1.1 Create `src/iec_cli/checkers/agents_hub_structure.py` — `AgentsHubStructure` class, checks `.agents/`, `.agents/instructions/`, `.agents/skills/` exist, reports missing items, registered via `@registry.register`
- [x] 1.2 Positive test: all three dirs present returns PASS [AHUB-001]
- [x] 1.3 Negative tests: `.agents/` missing returns FAIL with message [AHUB-002], `instructions/` missing returns FAIL [AHUB-003], `skills/` missing returns FAIL [AHUB-004], both subdirs missing reports both [AHUB-005]
- [x] 1.4 Registration test [AHUB-006]

## 2. secrets — implementation and proof

- [x] 2.1 Create `src/iec_cli/checkers/secrets.py` — `Secrets` class, scans text files for three patterns (private key, AWS key, credential assignment), skips `.git/node_modules/.venv/__pycache__`
- [x] 2.2 Positive test: clean files return PASS [SECR-001]
- [x] 2.3 Negative tests: AWS access key detected [SECR-002], private key marker detected [SECR-003], credential assignment detected [SECR-004]
- [x] 2.4 Boundary: files inside `.git/` are not scanned [SECR-005]
- [x] 2.5 Registration test [SECR-006]

## 3. Wiring

- [x] 3.1 Update `src/iec_cli/checkers/__init__.py` to import `agents_hub_structure`, `secrets`
- [x] 3.2 Update integration test to register and assert new checkers appear in output

## 4. Verify

- [x] 4.1 Run `uv run ruff check` — no lint errors
- [x] 4.2 Run `uv run ruff format --check` — no formatting issues
- [x] 4.3 Run `uv run pytest -v` — all 12 AC IDs proven (AHUB-001..006, SECR-001..006)
