## Why

`agents-size` counts every line of `AGENTS.md`, including a YAML front matter header. A repository that puts `type` and `title` in every Markdown file pays for it in the hub's line budget: the four header lines are four of the 50 lines the check allows. The intent-book repo hit this directly. Adding a header took `AGENTS.md` from 47 to 52 lines and failed `agents-size` until the file was cut to exactly 50, leaving no margin.

The limit exists to keep the hub short enough to load without crowding the context window. A header carries metadata, not instructions, and some agent hosts strip it before the model sees it. Counting it penalizes the practice for no benefit.

## What Changes

- `agents-size` skips a leading YAML front matter block when counting lines. The block starts when line 1 is `---` and ends at the next line that is exactly `---`.
- A file whose first line is `---` but has no closing `---` is counted in full. An unterminated header is a defect, not a header, so it gets no exemption.
- The result message states when front matter was excluded, so the number a developer sees matches the number they can count.
- The limit, the `ASE_AGENTS_MAX_LINES` override, and the default of 50 do not change.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `agents-size`: front matter lines do not count toward the limit.

## Impact

- Update: `src/iec_cli/checkers/agents_size.py`
- Update: `src/iec_cli/checkers/_shared.py` (new helper `front_matter_length`)
- Update: `tests/integration/test_checkers.py` (new scenarios AGSZ-007 to AGSZ-010)
- Behavior change for existing users: only files that start with `---` and close it are affected, and the result is a lower line count, so no repository that passes today starts failing.
- Out of scope: `file-size` (500-line limit on all `.md` files) still counts front matter. Four lines against 500 does not change outcomes in practice.
- Follow-up in intent-book: once this ships, `AGENTS.md` can regain the lines it gave up (the `docs:preview` command and the separate License bullet). Its CI installs `iec` from the default branch, so the change takes effect without a version bump.
