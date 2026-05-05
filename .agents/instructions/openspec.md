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

Run `/opsx:apply`. Work through tasks.md one task at a time. After each task or subtask is completed, IMMEDIATELY update tasks.md — change `- [ ]` to `- [x]` in the checkbox. The user tracks progress by watching the checkmarks accumulate. Do NOT batch completions at the end.

If a new task is needed during implementation, add it and **renumber the section** — never use suffixes like `2.2b` or `2.2.1`. Tasks stay clean, sequential, and reviewable. Update any artifact if you discover better approaches — no rigid phase gates.

**Tasks SHALL be self-contained.** When a task group produces code, the NEXT task MUST verify it with positive and negative proof. Never group all tests at the end. Each section of tasks.md is a self-contained vertical slice: implement → prove → move on. See `docs/testing-convention.md` for positive/negative proof requirements (equivalence classes and boundaries).

### 3. Archive

Run `/opsx:archive`. Delta specs merge into `openspec/specs/` (ADDED → appended, MODIFIED → replaced, REMOVED → deleted). The change folder moves to `changes/archive/YYYY-MM-DD-name/` to preserve history.

> **IMPORTANT:** The `openspec instructions specs` template shows bare `#### Scenario: <name>` without AC IDs or `**Test:**` fields. The OpenSpec template is generic and does NOT enforce ase-cli conventions. You MUST add `[PREFIX-NNN]` AC IDs to every scenario heading and a `**Test:**` field to every scenario yourself. See below.

## Acceptance Criteria (AC IDs)

Every spec scenario MUST have an AC ID in `[PREFIX-NNN]` format, embedded in the scenario heading:

```markdown
#### Scenario: Points earned on delivery [LP-001]

**Test:** Unit

- **GIVEN** an order has been marked as delivered
- **WHEN** the order total is at least $5.00
- **THEN** 1 point per dollar is awarded to the customer
```

Rules:
- The prefix maps to the spec or capability name (e.g., `LP` for Loyalty Points, `DRAM` for DRAM module)
- IDs are unique within the project, zero-padded, sequential per prefix
- Once assigned, an ID SHALL NOT be reused or renumbered
- Removed scenarios keep their IDs in archive history — do not renumber remaining scenarios
- Every scenario MUST have a `**Test:**` field declaring the required test layer
- Every non-Manual AC MUST have positive and negative proof via its significant equivalence classes and boundaries
- See `docs/testing-convention.md` for the full test layer taxonomy and traceability contract

## Test Traceability

Tests reference AC IDs to enable traceability:

```python
# pytest marker
@pytest.mark.ac("LP-001")
def test_points_earned_on_delivery():
    ...

# Fallback comment (any language)
# AC: LP-001
def test_points_earned_on_delivery():
    ...
```

Tests that do NOT prove acceptance criteria SHALL carry a category marker:

```python
@pytest.mark.baseline  # Coverage-threshold regression protection
@pytest.mark.sanity     # Toolchain/environment readiness
```

Framework-specific marker formats and the full traceability contract are defined in `docs/testing-convention.md`.

ase-cli's `test-traceability` check cross-references AC IDs in specs against test markers.
