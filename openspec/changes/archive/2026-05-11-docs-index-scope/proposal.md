# Proposal: docs-index-scope — enforce per-directory INDEX.md scope

## Why

`docs-index-exists` proves every directory has an `INDEX.md`. `docs-index-stale` proves each index matches its directory contents. Neither catches the most common drift in practice: a top-level `INDEX.md` that lists files from sub-directories ("decisions/0001-x.md", "decisions/0002-y.md", ...) — duplicating the sub-INDEX and silently rotting as sub-directory contents change. The book repo's `docs/INDEX.md` exhibits exactly this pattern today, plus an "agent instruction hub" block linking to `../AGENTS.md` and `../.agents/...` files that don't belong in the docs tree map at all.

The rule is implied by two principles already in `plan.md` (ase-book):

- "Documents form a hypergraph, not a tree. Agents and humans pick the relevant context via links and skip the rest. Fast retrieval at every depth is part of the design, not an afterthought."
- "Every `docs/` directory has a `README.md` ... and an `INDEX.md` (agent-facing map, context economy)."

If every directory has its own INDEX, the top-level INDEX points at child INDEXes; it doesn't enumerate their contents.

## What Changes

- **New checker** `docs-index-scope` (severity WARN). For each `INDEX.md` under `docs/`, parses Markdown inline links and verifies each target is either a same-directory file or an immediate `subdir/INDEX.md` / `subdir/README.md` pointer. Flags deeper paths, parent paths (`../`), and absolute URLs.
- **Shared link parser**: promote `_LINK_RE` from `docs_index_stale.py` into the existing `_shared.py` module (created in the previous change) and rename to `LINK_RE`. `docs_index_stale.py` and the new `docs_index_scope.py` both import it. One regex, two consumers.

## Capabilities

### New Capabilities

- `docs-index-scope`: enforces per-directory INDEX scope; WARN with offender list.

### Modified Capabilities

- `docs-index-stale`: no behavior change. Just imports `LINK_RE` from `_shared` instead of defining it locally.

## Impact

- **New module**: `src/ase_cli/checkers/docs_index_scope.py`
- **Modified modules**: `src/ase_cli/checkers/_shared.py` (export `LINK_RE`), `docs_index_stale.py` (import it), `__init__.py` (register new checker)
- **New spec**: `openspec/specs/docs-index-scope/spec.md` with DISO-001..008
- **Tests**: 9 new unit tests in `tests/test_docs_checkers.py`
- **Downstream**: ase-book's `docs/INDEX.md` requires a cleanup commit to comply. The cross-tree pointers it currently holds move into `docs/README.md` prose.
- **No new dependencies**.
