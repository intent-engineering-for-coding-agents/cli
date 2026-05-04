# update-index

## Purpose

Scan the `docs/` directory and regenerate all index/listing files to match current files on disk.

## When to Run

- After creating any new file under `docs/`
- After renaming or deleting any file under `docs/`
- When `docs/INDEX.md` might be stale

## What It Updates

| File | What it contains |
|---|---|
| `docs/INDEX.md` | Every file under `docs/` with a one-line description |
| `docs/decisions/README.md` | All ADR files with status and date |
| `docs/design/README.md` | All design doc files with status and date |

## How to Run

Read the current state of `docs/`, then update each listing file:

### Step 1 — Scan docs/

List every file under `docs/` recursively. For each file, determine which listing file(s) it belongs in.

### Step 2 — Update docs/INDEX.md

Regenerate the table. Every file gets one row:

```markdown
| [filename](relative/path) | Description from file content or filename |
```

The description should be one line extracted from the file's first heading or derived from the filename if no heading exists. Exclude `INDEX.md` from the listing of the root (it IS the file). Exclude `README.md` files from their own directory listings (they render on GitHub automatically).

### Step 3 — Update docs/decisions/README.md

Regenerate the table. For each `docs/decisions/NNNN-title.md`:

```markdown
| [number](filename.md) | Title (from file's first heading) | status (from file's Status field) | date (from file's Date field) |
```

### Step 4 — Update docs/design/README.md

Regenerate the table. For each `docs/design/*.md` that is not `README.md`:

```markdown
| filename.md | Feature name (from heading) | status | date |
```

### Step 5 — Verify

Read back each updated file to confirm no broken links, no missing entries, no orphaned rows.
