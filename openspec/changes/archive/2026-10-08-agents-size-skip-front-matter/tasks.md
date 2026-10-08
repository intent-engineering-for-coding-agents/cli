# Tasks: agents-size-skip-front-matter

## 1. Implementation

- [x] 1.1 Add `front_matter_length(lines)` to `src/iec_cli/checkers/_shared.py`
- [x] 1.2 Use it in `src/iec_cli/checkers/agents_size.py` and extend the PASS and FAIL messages when the length is greater than 0

## 2. Proof

- [x] 2.1 Positive: 4-line header plus 48 content lines, limit 50, PASS [AGSZ-007]
- [x] 2.2 Negative: 4-line header plus 51 content lines, FAIL [AGSZ-008]
- [x] 2.3 Negative: unterminated header, 52 lines, FAIL with the full count [AGSZ-009]
- [x] 2.4 Negative: `---` rule at line 20 without a leading header, FAIL with the full count [AGSZ-010]
- [x] 2.5 Existing AGSZ-001 to AGSZ-006 still pass unchanged

## 3. Docs

- [x] 3.1 Update `tests/ac-registry.md`: the `AGSZ` max used becomes 010
- [x] 3.2 Run `uv run pytest` and `iec check` in this repo
- [x] 3.3 Archive the change with `/opsx:archive`
