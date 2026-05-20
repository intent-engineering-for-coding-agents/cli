# Design: Spec Quality Checks

## File Discovery

`find_spec_files(path)` scans two locations:
- `openspec/specs/**/*.md` — canonical specs (merged after archive)
- `openspec/changes/*/specs/**/*.md` — active change specs (any change dir that is not `archive/`)

Archived change folders (`openspec/changes/archive/`) are excluded. They are historical and were already valid when merged.

## spec-ac-ids

Split: `re.finditer(r"^#{3,6}\s+Scenario:\s+.+$", content, re.MULTILINE)` finds all scenario headings. For each heading, check for `\[[A-Z][A-Z0-9]+-\d+\]`. Report all missing ACs in a single FAIL result.

## spec-test-category

Split: `re.compile(r"(^#{3,6}\s+Scenario:\s+.+$)", re.MULTILINE).split(content)` with a capturing group produces alternating `[pre, heading, body, heading, body, ...]` parts. For each body, check for `^\*\*Test:\*\*`. Report all missing fields in a single FAIL result.

## Severity

Both checks: `Severity.HIGH`. AC IDs are load-bearing for Phase G traceability; `**Test:**` fields are required by convention.
