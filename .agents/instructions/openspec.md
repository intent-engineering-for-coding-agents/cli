# OpenSpec Workflow

All features in ase-cli are spec-driven. Every change goes through OpenSpec: propose → apply → archive.

## Setup

OpenSpec requires Node.js 20.19+. Install globally once per machine:

```
npm install -g @fission-ai/openspec@latest
```

Then initialize in the project (already done — committed as `.opencode/`):

```
openspec init --tools opencode
openspec update            # Refresh after upgrades
```

The generated `.opencode/` directory contains slash commands and skills. These are committed to the repo so every developer gets them — like `.github/copilot-instructions.md` or `CLAUDE.md`, they're generated pointers, not authored duplicates.

## Quick Reference

| Command | What it does |
|---|---|
| `/opsx:propose <idea>` | Create a change folder with proposal, specs, design, tasks |
| `/opsx:apply` | Implement tasks, checking them off as you go |
| `/opsx:archive` | Merge delta specs into `openspec/specs/`, move change to archive |

## Directory Layout

```
openspec/
├── changes/                          # Active and proposed changes
│   ├── add-dark-mode/                # One directory per change
│   │   ├── proposal.md               # Why and what
│   │   ├── design.md                 # Technical approach
│   │   ├── tasks.md                  # Implementation checklist
│   │   └── specs/                    # Delta specs (ADDED/MODIFIED/REMOVED)
│   └── archive/                      # Completed changes
│       └── YYYY-MM-DD-add-dark-mode/ # Dated, preserved for history
└── specs/                            # Canonical specs (source of truth)
```

## How a Change Works

### 1. Propose

Run `/opsx:propose <what-you-want-to-build>`. This creates the change folder with all planning artifacts. Artifacts build on each other: proposal (why) → specs (what) → design (how) → tasks (steps).

### 2. Apply

Run `/opsx:apply`. Work through tasks.md, checking them off. Update any artifact if you discover better approaches — no rigid phase gates. OpenSpec operates on actions, not locked phases.

### 3. Archive

Run `/opsx:archive`. Delta specs merge into `openspec/specs/` (ADDED → appended, MODIFIED → replaced, REMOVED → deleted). The change folder moves to `changes/archive/YYYY-MM-DD-name/` to preserve history.

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
