## Context

Change 004 added `docs-readme-exists`, `docs-index-exists`, and `docs-index-stale` checkers following a standard pattern: one class per file, `@registry.register`, `check(path)` returns `CheckResult`. Change 005 adds two more checkers in the same pattern, targeting `docs/decisions/`.

`docs/decisions/` in ase-cli holds 6 MADR-format ADRs. The MADR convention requires a 4-digit numeric prefix in the filename and specific section headings. Currently nothing enforces this, so a malformed ADR would silently pass validation.

## Goals / Non-Goals

**Goals:**
- `adr-format`: reject ADR files with wrong filename pattern, missing required sections, or invalid status values
- `adr-index`: reject a missing or incomplete `docs/decisions/README.md`

**Non-Goals:**
- Validating ADR prose quality or decision content
- Checking ADRs outside `docs/decisions/`
- Enforcing the `## Pros and Cons` section (optional in MADR)
- Parsing or validating linked files referenced inside ADR content

## Decisions

**Filename pattern: `^\d{4}-[a-z0-9-]+\.md$`**
The 4-digit prefix is the MADR convention and is what enables stable numeric references. Rejecting anything that doesn't match (other than `README.md` and `INDEX.md`) ensures no non-ADR files accumulate in `docs/decisions/` unnoticed. Alternative: warn instead of fail — rejected because the filename convention is structural, not stylistic.

**Required sections: `## Context and Problem Statement` and `## Decision Outcome` only**
These two are the load-bearing sections — without them an ADR cannot be read as a decision record. The options section and consequences section are common but not required to extract the decision. Alternative: require all MADR sections — rejected as over-prescriptive for a lint tool.

**Title heading: required, numbered prefix optional**
Every ADR must have a `#` heading as its first non-empty line — without it the file isn't a readable decision record. If the heading uses the numbered style `# ADR-NNNN: Title`, the number must match the filename prefix (a mismatch indicates copy-paste error). A plain title like `# My Decision` is also valid and is the norm for YAML front matter style ADRs. Alternative: require `# ADR-NNNN:` for all ADRs — rejected because MADR's own YAML template does not include the number in the heading.

**Status field: accept both bullet style and YAML front matter; prefix-match for `superseded`**
The MADR standard has two generations: older ADRs use `* Status: <value>` bullet lines; newer ADRs use `status: <value>` in YAML front matter. Both are valid. The checker accepts either format. An ADR with neither present is a violation. ase-cli's existing ADRs use the bullet style and will be migrated to YAML front matter as part of this change. Valid base words: `accepted`, `deprecated`, `superseded`, `proposed`. The check uses a prefix match so that `superseded by [ADR-0005](0005-example.md)` — the canonical MADR form for a superseded decision — passes without requiring an exact match.

**Fixture files for content-sensitive tests**
Tests for `adr-format` require real file content (headings, sections, front matter) — inline string construction is fragile and unreadable at scale. Fixture files in `tests/fixtures/adr/` represent canonical examples of each format variant and violation case. Tests copy the appropriate fixture into `tmp_path/docs/decisions/NNNN-name.md` with the correct filename, keeping content and filename concerns separate. Fixture files: `valid_bullet.md`, `valid_yaml.md`, `missing_title.md`, `title_mismatch.md`, `missing_context.md`, `missing_decision.md`, `missing_status.md`, `invalid_status_bullet.md`, `invalid_status_yaml.md`.

**Both checkers return PASS when `docs/decisions/` is absent or empty**
A missing or empty `docs/decisions/` is a valid new-project state — the directory has been scaffolded but no decisions have been recorded yet. There are no ADRs to validate or index, so both checks trivially pass. Neither checker should penalise a project that hasn't yet made any architectural decisions. The checks become meaningful only once `NNNN-*.md` files appear in the directory.

## Risks / Trade-offs

**Dual status format parsing** → The checker must detect both `* Status:` bullet lines and `status:` YAML front matter. Front matter is delimited by `---` at the start of the file; the checker reads lines between the first and second `---` to extract `status:`. Bullet-style is detected by scanning non-front-matter lines. If both are present (malformed file), the YAML front matter value takes precedence. Mitigation: strip whitespace around values in both formats.

**README.md link parsing** → The index check parses Markdown links from README.md using the existing `LINK_RE` pattern from `_shared.py`. This covers the standard table format used in ase-cli. Malformed links in README.md (e.g., HTML anchors) would not be detected as links, potentially causing false FAIL. Mitigation: the standard README format is a Markdown table with `[NNNN](NNNN-title.md)` links — the LINK_RE covers this exactly.
