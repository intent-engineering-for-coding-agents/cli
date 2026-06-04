# Check Reference

All checks run by `iec check`. Each check carries a **maturity** label:

- **ci-enforced** — exits non-zero on failure; suitable as a hard CI gate.
- **advisory** — exits with a warning (exit 1); best run locally or in non-blocking CI mode.

## Check catalogue

| Check | Description | Maturity | Default status on violation |
|---|---|---|---|
| `agents-exists` | AGENTS.md present at repo root | ci-enforced | FAIL |
| `agents-size` | AGENTS.md under N lines (default 50; env: `ASE_AGENTS_MAX_LINES`) | ci-enforced | FAIL |
| `agents-links` | Every link in AGENTS.md has descriptive text (not a bare URL) | advisory | WARN |
| `agents-hub-structure` | `.agents/` has `instructions/` and `skills/` subdirectories | ci-enforced | FAIL |
| `docs-readme-exists` | `docs/README.md` present with architecture overview | ci-enforced | FAIL |
| `docs-index-exists` | Every `docs/` subdirectory has an `INDEX.md` | advisory | WARN |
| `docs-index-stale` | `INDEX.md` entries match actual files (no broken links, no orphans) | advisory | WARN |
| `docs-index-scope` | Each `INDEX.md` maps only its own directory, no cross-directory entries | advisory | WARN |
| `adr-format` | All ADRs follow MADR template (`docs/decisions/NNNN-title.md`) | ci-enforced | FAIL |
| `adr-index` | `docs/decisions/README.md` exists and lists all ADRs | ci-enforced | FAIL |
| `spec-ac-ids` | Every spec scenario has a `[PREFIX-NNN]` AC ID | ci-enforced | FAIL |
| `spec-test-category` | Every scenario has a `Test-type:` field | ci-enforced | FAIL |
| `spec-size` | Spec files under configurable line limit (default 500; env: `ASE_FILE_MAX_LINES`) | advisory | WARN |
| `file-size` | All `.md` files under configurable line limit (default 500; env: `ASE_FILE_MAX_LINES`) | advisory | WARN |
| `secrets` | No plaintext secrets (keys, tokens, passwords) in tracked files | ci-enforced | FAIL |
| `test-traceability` | Every non-Manual spec AC ID has at least one `@pytest.mark.<AC_ID>` test marker | ci-enforced | FAIL |
| `test-coverage` | Non-Manual ACs have both a positive and a negative test proof | advisory | WARN |
| `tasks-complete` | Active change folder's `tasks.md` has no unchecked `- [ ]` items | ci-enforced | FAIL |
| `change-archived` | Completed change folders are archived (not left live on trunk) | ci-enforced | FAIL |

## Exit codes

| Exit code | Meaning |
|---|---|
| `0` | All checks passed |
| `1` | One or more advisory warnings (no gate failures) |
| `2` | One or more ci-enforced failures |

## CI usage

The recommended CI pattern gates on exit code ≤ 1 (pass or advisory warnings only):

```yaml
- name: Self-check (fail on errors, allow warnings)
  run: iec check; code=$?; [ $code -le 1 ]
```

To gate on all checks including advisory ones, use `[ $code -eq 0 ]`.

## Configuration

Environment variables control configurable limits:

| Variable | Default | Affects |
|---|---|---|
| `ASE_AGENTS_MAX_LINES` | `50` | `agents-size` |
| `ASE_FILE_MAX_LINES` | `500` | `file-size`, `spec-size` |
