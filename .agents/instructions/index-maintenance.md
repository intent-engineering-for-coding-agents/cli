# docs/ Index Maintenance

Whenever you create, rename, or delete any file under `docs/`, you MUST update the relevant index and listing files.

## Files to Update

| When you change... | Update... |
|---|---|
| Any file under `docs/` (create, rename, delete) | `docs/INDEX.md` — add/update/remove the file entry |
| Any file under `docs/decisions/` (create, rename, delete) | `docs/decisions/README.md` — add/update/remove the ADR row |
| Any file under `docs/design/` (create, rename, delete) | `docs/design/README.md` — add/update/remove the design doc row |

## Index Entry Format

### docs/INDEX.md

Each entry is a table row:
```
| [relative-link](path) | One-line description of what the file contains |
```

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

## Why

Agents load `docs/INDEX.md` first for context economy. A stale index — broken links, missing entries, orphans — causes the agent to waste context loading wrong files or missing right ones. The `update-index` skill can regenerate these automatically.
