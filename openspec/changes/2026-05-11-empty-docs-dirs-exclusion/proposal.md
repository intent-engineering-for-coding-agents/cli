# Proposal: Exempt effectively-empty docs/ subdirectories from presence checks

## Why

`docs-readme-exists` (FAIL) and `docs-index-exists` (WARN) currently flag *every* subdirectory of `docs/`, including placeholder dirs that hold nothing but a `.gitkeep`. The ase-book repo hit this immediately: `docs/design/` is a reserved placeholder that hasn't accumulated content yet, and CI failed solely because of it. Mandating `README.md` + `INDEX.md` for empty placeholder directories is noise — there is nothing to document.

The sibling `docs-index-stale` checker has already taken this position: it explicitly ignores `.gitkeep` (DINS-005). This change extends the same intent to the two presence checkers.

## What Changes

- New shared helper `src/ase_cli/checkers/_shared.py` with `is_effectively_empty(dirpath: Path) -> bool`. Returns `True` when the directory's recursive subtree contains no regular files except entries whose name begins with `.` (e.g. `.gitkeep`, `.hidden`, `.DS_Store`).
- `docs-readme-exists` skips effectively-empty subdirectories before reporting a missing `README.md`.
- `docs-index-exists` skips effectively-empty subdirectories before reporting a missing `INDEX.md`.
- New scenarios on each checker's spec (DRME-006, DINE-006) covering the four cases: `.gitkeep`-only, dotfiles-only, nested empty subdir, and substantive content alongside `.gitkeep` (still flagged).

## Capabilities

### Modified Capabilities

- `docs-readme-exists`: same as before, but exempts directories whose subtree contains no non-dot regular files.
- `docs-index-exists`: same as before, with the same exemption.

### New Capabilities

*(None — internal helper module only.)*

## Impact

- **New module**: `src/ase_cli/checkers/_shared.py`
- **Modified modules**: `src/ase_cli/checkers/docs_readme_exists.py`, `docs_index_exists.py`
- **Tests**: New scenarios in `tests/test_docs_checkers.py`; two existing tests updated to use a substantive file in the subdir (previously they relied on empty subdirs being flagged, which is exactly the behavior we are changing).
- **Specs updated**: `openspec/specs/docs-readme-exists/spec.md`, `openspec/specs/docs-index-exists/spec.md`
- **Downstream**: The ase-book repo's `docs/design/` placeholder stops failing CI.
- **No new dependencies**.
