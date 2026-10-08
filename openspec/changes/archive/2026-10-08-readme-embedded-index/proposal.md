## Why

Every `docs/` directory currently needs two files that list the same content: an `INDEX.md` (the agent-facing map) and a `README.md` (the human-facing listing). The two lists drift apart as soon as a commit updates only one of them, and the book's own `docs/decisions/` lists the same two ADRs in both.

One `README.md` per directory can serve both readers: a few opening lines for people on a Git host, then a marker-delimited index block with one row per file. The agent reads the block as the map, and a script reads exactly the lines between the markers.

## What Changes

- An index block in `README.md`, delimited by `<!-- index:start -->` and `<!-- index:end -->` on their own lines, counts as the directory's index.
- `docs-index-exists` passes a directory that has either an `INDEX.md` or a `README.md` with a terminated index block.
- `docs-index-stale` checks the rows of the block against the directory's files. `README.md` itself is not an orphan when it hosts the block.
- `docs-index-scope` applies the existing scope rule to links inside the block only. Links elsewhere in the README are ignored.
- A standalone `INDEX.md` keeps working and wins when both forms exist. Existing adopters need no change.
- Messages become form-neutral ("All docs/ directories have an index", "Out-of-scope index links").

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `docs-index-exists`: a README.md index block satisfies the presence rule.
- `docs-index-stale`: the block is cross-referenced like an INDEX.md.
- `docs-index-scope`: the block is scope-checked like an INDEX.md.

## Impact

- Update: `src/iec_cli/checkers/_shared.py` (new `embedded_index_lines`, `index_source`)
- Update: `src/iec_cli/checkers/docs_index_exists.py`, `docs_index_stale.py`, `docs_index_scope.py`
- Update: `tests/test_docs_checkers.py` (DINE-007 to DINE-009, DINS-008 to DINS-011, DISO-009 to DISO-011)
- Behavior change for existing users: none for repositories that keep `INDEX.md`. Result message text changes wording only.
- Out of scope: `iec init` still scaffolds `INDEX.md`, and the `update-index` skill text still describes the INDEX form. Both follow in a later change.
