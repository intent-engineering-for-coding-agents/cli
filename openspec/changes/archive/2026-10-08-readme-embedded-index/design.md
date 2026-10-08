## Context

The three checkers each hard-code `dirpath / "INDEX.md"` and read the whole file. A shared lookup lets them treat both forms the same way.

## Decisions

### Decision 1: One lookup, `index_source(dirpath)`

`index_source` returns `(file, lines, embedded)` or None. A standalone `INDEX.md` is returned first, with all its lines. Otherwise `README.md` is searched for the markers and the lines between them are returned. The checkers then run unchanged logic over `lines`.

### Decision 2: INDEX.md wins when both exist

Two indexes in one directory is the drift this change removes, but the checkers do not police it. They check the one that wins and ignore the README block. A later check could warn on the pair.

### Decision 3: Markers are fixed strings

`<!-- index:start -->` and `<!-- index:end -->`, matched on trimmed whole lines. A start marker with no end marker means no index, so the directory is reported as missing one. A fixed pair is simple to write by hand, and it is exactly what a regeneration tool would need later.

### Decision 4: The host file is not an orphan

For an embedded block, `README.md` is excluded from the orphan check, as `INDEX.md` is today. Rows may still link it.

## Risks

- Markers drift in spelling (`<!-- Index:Start -->`). The result is a "missing index" warning, which names the directory and is easy to fix.
