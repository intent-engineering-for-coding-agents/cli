# docs/ Index Maintenance

Whenever you create, rename, or delete any file under `docs/`, you MUST update the index and listing files **of that file's directory** — not the top-level `docs/INDEX.md`.

## INDEX.md scope — flat per directory

Every `docs/` directory has its own `INDEX.md`, and that INDEX maps **only its own directory**. A link inside an `INDEX.md` may point to:

- A **same-directory file**, e.g. `[A](a.md)` — no `/` in the path.
- An **immediate child pointer**, e.g. `[Decisions](decisions/INDEX.md)` or `[Decisions](decisions/README.md)` — the child's own INDEX/README, nothing deeper.

Anything else — `decisions/0001-x.md`, `../AGENTS.md`, `https://example.com/...` — belongs in `README.md` prose, not in the INDEX table. The CLI enforces this via the `docs-index-scope` checker (WARN).

The principle: documents form a hypergraph navigated by following sub-INDEX pointers. A top-level INDEX that enumerates everything below it duplicates the sub-INDEXes and rots silently.

## Files to Update

| When you change... | Update... |
|---|---|
| A file directly in `docs/` (not in a sub-dir) | `docs/INDEX.md` |
| A file in `docs/decisions/` | `docs/decisions/INDEX.md` **and** `docs/decisions/README.md` (the latter for the human-facing ADR row) |
| A file in `docs/<other-subdir>/` | that sub-dir's `INDEX.md` (and its `README.md` listing if it has one) |
| A new sub-directory gains its first substantive file | add `INDEX.md` + `README.md` in the new sub-dir; add a single pointer row to it in the parent `INDEX.md` |

## Index Entry Format

### Any INDEX.md

Each entry is a table row:
```
| [relative-link](path) | One-line description of what the file contains |
```

Where `path` is either a same-dir filename or a `subdir/INDEX.md` / `subdir/README.md` pointer (see scope rule above).

### docs/decisions/README.md

Each entry is a table row:
```
| [number](filename.md) | Title | status | YYYY-MM-DD |
```

### docs/design/README.md

Each entry is a table row:
```
| filename.md | Feature name | status | YYYY-MM-DD |
```

## Empty directories

A directory under `docs/` that holds no substantive content — only a `.gitkeep`, or nothing at all — does **not** need `README.md` or `INDEX.md`. `ase check` (>= the empty-dirs-exclusion change) skips such placeholders. Create the two files the moment the directory gets its first real file, and add the new dir's entry to `docs/INDEX.md` at the same time.

## Why

Agents load `docs/INDEX.md` first for context economy. A stale index — broken links, missing entries, orphans — causes wasted context and missed files. The `update-index` skill can regenerate these automatically.
