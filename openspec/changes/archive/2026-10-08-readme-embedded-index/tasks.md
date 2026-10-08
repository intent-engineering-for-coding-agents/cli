# Tasks: readme-embedded-index

## 1. Implementation

- [x] 1.1 Add `embedded_index_lines` and `index_source` to `src/iec_cli/checkers/_shared.py`
- [x] 1.2 Use `index_source` in `docs_index_exists.py`, `docs_index_stale.py`, and `docs_index_scope.py`, with form-neutral messages

## 2. Proof

- [x] 2.1 Positive: README block counts as an index [DINE-007]
- [x] 2.2 Negative: README without a block, and an unterminated block, warn [DINE-008] [DINE-009]
- [x] 2.3 Block matches the directory, host README is not an orphan [DINS-008]
- [x] 2.4 Orphan and broken link next to a block warn [DINS-009] [DINS-010]
- [x] 2.5 INDEX.md wins over a README block [DINS-011]
- [x] 2.6 Deeper path in a block warns, outside links ignored, child README pointer passes [DISO-009] [DISO-010] [DISO-011]

## 3. Docs

- [x] 3.1 Update `tests/ac-registry.md`: DINE 009, DINS 011, DISO 011
- [x] 3.2 Run `uv run python -m pytest`, `ruff check`, `ruff format --check`
- [x] 3.3 Archive the change with `openspec archive`
