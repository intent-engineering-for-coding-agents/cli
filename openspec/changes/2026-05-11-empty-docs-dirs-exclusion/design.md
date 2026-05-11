# Design: Effectively-empty docs/ subdirectories

## Context

`docs/` conventions require both `README.md` and `INDEX.md` in every subdirectory. That convention is sound when the directory has content — `README.md` is the human-facing overview that renders on GitHub, `INDEX.md` is the agent-facing file map. It is not sound for *placeholder* directories that hold only `.gitkeep` to keep the path tracked in git.

The book repo CI already surfaced this: `docs/design/` is reserved for future feature design docs and contains a single `.gitkeep`. The current checker rule treats it identically to a populated directory and fails the build.

## Goals / Non-Goals

**Goals:**
- A directory whose subtree contains no substantive content does not require `README.md` or `INDEX.md`.
- Dotfile entries (`.gitkeep`, `.hidden`, `.DS_Store`) are not substantive content.
- A real file alongside `.gitkeep` *is* substantive — the rule does not become a loophole.
- Behavior matches the existing `docs-index-stale` treatment of `.gitkeep` (DINS-005).

**Non-Goals:**
- Configurable allow-list of "ignored" filenames.
- Skipping non-empty directories that the user *wishes* would be skipped (e.g. dirs with only an out-of-scope binary). If you have substantive content, you owe it a README/INDEX.
- Changing the severity or status semantics of either checker.

## Decisions

### Decision 1: One shared helper, used by both checkers

**Chosen**: `src/ase_cli/checkers/_shared.py::is_effectively_empty(dirpath)`. Both presence checkers call it.

**Rationale**: The rule is identical for the two checkers and likely to be referenced by future ones. Extracting it now avoids drift. The leading underscore signals an internal module — it is not part of the public checker registry.

### Decision 2: Recursive subtree, not single directory

**Chosen**: Walk `dirpath.rglob("*")` and look for any regular file whose name does not start with `.`.

**Rationale**: A user might create `docs/design/wip/.gitkeep` — `docs/design/` itself has no files, only a subdir. We want `docs/design/` skipped in that case too. The recursive walk handles this naturally and matches the recursive style already used by both checkers (`docs_dir.rglob("*")` on line 21 of each).

### Decision 3: Dotfile heuristic by name prefix

**Chosen**: A file is "non-substantive" if `entry.name.startswith(".")`. This covers `.gitkeep`, `.hidden`, `.DS_Store`, `.keep`, etc.

**Rationale**: Simple, language-agnostic, and matches POSIX hidden-file convention. The book convention is `.gitkeep`; broadening to any dotfile is a small generalization that absorbs editor/OS noise without surprise.

### Decision 4: Short-circuit on first substantive file

**Chosen**: Return `False` the moment a non-dot regular file is seen anywhere in the subtree.

**Rationale**: Most placeholder dirs are tiny; most populated dirs have content near the root. Either way, the walk terminates fast. No special-casing needed.

## Risks / Trade-offs

- **[Trade-off]** A directory that contains *only* a binary blob with a dotfile name (e.g. `.tarball`) would be classified as empty. Unrealistic in `docs/`; we accept.
- **[Trade-off]** Symlinks are followed by `rglob` by default. A pathological symlink loop under `docs/` would hang. Out of scope — `docs/` does not contain symlinks in any known project.
- **[Risk]** Two existing scenarios (`DRME-002`/`DRME-003`, `DINE-002`/`DINE-003`) were authored against empty-dir test fixtures. They are updated to include a real file in the subdir; the semantic claim of those scenarios is preserved (a populated subdir without README/INDEX is still flagged), but the wording in the spec is left intentionally vague about whether the subdir is empty or populated so that DRME-006/DINE-006 carry the precise rule.
