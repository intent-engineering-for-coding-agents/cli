# iec-cli

**Intent Engineering practice validation CLI** — deterministic checks for agentic software engineering repos.

`iec check` scans a repository for missing structure, broken spec conventions, and untraced acceptance criteria. No AI required. Pure Python, runs anywhere.

## Why

Coding agents drift. They skip `AGENTS.md`, write specs without AC IDs, implement without marking tasks complete. `iec check` catches this at the file level before it becomes a review conversation.

## Installation

```bash
# From a local checkout (requires uv)
git clone <repo-url>
cd intent-cli
uv sync
uv run iec --version
```

## Quick start

```bash
# Scaffold Intent Engineering structure in the current repo
iec init

# Run all deterministic checks
iec check

# Scope to a subdirectory
iec check --path src/
```

## Checks

`iec check` runs 19 checks split across two maturity tiers:

| Maturity | Behaviour | Typical use |
|---|---|---|
| **ci-enforced** | `FAIL` → exit 2; blocks CI | Hard gate on every PR |
| **advisory** | `WARN` → exit 1; non-blocking | Local runs, periodic audits |

### CI-enforced (hard gates)

| Check | What it validates |
|---|---|
| `agents-exists` | AGENTS.md present at repo root |
| `agents-size` | AGENTS.md under N lines (TOC, not encyclopedia) |
| `agents-hub-structure` | `.agents/` has `instructions/` and `skills/` subdirs |
| `docs-readme-exists` | `docs/README.md` present with architecture overview |
| `adr-format` | All ADRs follow MADR template |
| `adr-index` | `docs/decisions/README.md` lists all ADRs |
| `spec-ac-ids` | Every spec scenario has a `[PREFIX-NNN]` AC ID |
| `spec-test-category` | Every scenario has a `Test-type:` field |
| `secrets` | No plaintext secrets in tracked files |
| `test-traceability` | Every non-Manual AC ID has a `@pytest.mark.<AC_ID>` test |
| `tasks-complete` | Active change folder has no unchecked tasks before merge |
| `change-archived` | Completed change folders are archived, not left on trunk |

### Advisory (non-blocking)

| Check | What it validates |
|---|---|
| `agents-links` | Links in AGENTS.md have descriptive text |
| `docs-index-exists` | Every `docs/` subdirectory has an `INDEX.md` |
| `docs-index-stale` | `INDEX.md` entries match actual files |
| `docs-index-scope` | Each `INDEX.md` maps only its own directory |
| `spec-size` | Spec files under configurable line limit |
| `file-size` | All `.md` files under configurable line limit |
| `test-coverage` | Non-Manual ACs have positive + negative test proofs |

See [docs/checks.md](docs/checks.md) for exit codes, configuration, and CI integration patterns.

## Exit codes

| Exit code | Meaning |
|---|---|
| `0` | All checks passed |
| `1` | Advisory warnings only |
| `2` | One or more hard failures |

## CI integration

```yaml
- name: Self-check (fail on errors, allow warnings)
  run: iec check; code=$?; [ $code -le 1 ]
```

## Configuration

| Environment variable | Default | Affects |
|---|---|---|
| `ASE_AGENTS_MAX_LINES` | `50` | `agents-size` |
| `ASE_FILE_MAX_LINES` | `500` | `file-size`, `spec-size` |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, the spec-driven workflow, and how to add a new checker.

## License

Apache 2.0. See [LICENSE](LICENSE).
