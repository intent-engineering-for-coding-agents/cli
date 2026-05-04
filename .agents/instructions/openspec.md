# OpenSpec Workflow

All features in ase-cli are spec-driven. Every change starts with an OpenSpec proposal.

## Directory Layout

```
openspec/
├── changes/            # Active and proposed changes
│   ├── NNN-change-id/  # One directory per change
│   │   ├── proposal.md
│   │   ├── design.md
│   │   ├── tasks.md
│   │   └── specs/      # Spec deltas for this change
│   └── archive/        # Completed changes (historical record)
└── specs/              # Canonical specs (current system behavior)
```

## Creating a Change

1. Choose the next NNN number (check `openspec/changes/` for the highest)
2. Create `openspec/changes/NNN-short-id/` with:
   - `proposal.md` — What, why, scope, non-goals
   - `design.md` — Technical decisions, trade-offs
   - `tasks.md` — Implementation tasks, breaking work into checkable units
   - `specs/` — Spec deltas showing requirement changes

## Acceptance Criteria (AC IDs)

Every spec scenario MUST have an AC ID in `[AC-NNN]` format:

```markdown
### Requirement: Something

#### Scenario: Name
[AC-001] Description of expected behavior
**Given** precondition
**When** action
**Then** expected outcome

**Test:** Unit | Integration | Manual
```

Rules:
- AC IDs are unique within the spec, sequential from 001
- Every AC must have a `**Test:**` field (Unit, Integration, or Manual)
- `Manual` tests are the exception — only when automation is impossible
- Every non-Manual AC must have positive AND negative proof in tests/

## Test Traceability

Tests reference AC IDs to enable traceability:

```python
# Python test with pytest marker
@pytest.mark.ac("SPEC-001")
def test_session_expiration():
    ...

# Or inline comment (fallback)
# AC: SPEC-001
def test_session_expiration():
    ...
```

ase-cli's `test-traceability` check cross-references AC IDs in specs against test markers.
