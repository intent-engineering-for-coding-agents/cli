## Context

`adr_format.py` already has `_parse_front_matter`, which returns a dict and the body lines. `agents-size` only needs a count, and importing the ADR parser into an unrelated checker couples the two.

## Decisions

### Decision 1: A small shared helper that returns the header length

Add `front_matter_length(lines: list[str]) -> int` to `_shared.py`. It returns 0 when `lines[0].strip()` is not `---` or when no closing `---` follows. Otherwise it returns the number of lines through the closing marker. `agents-size` subtracts it from the total.

Alternative considered: reuse `_parse_front_matter` from `adr_format.py`. Rejected because it parses values the size check does not need, and making `agents-size` depend on the ADR checker module is the wrong direction. Consolidating the two parsers is a reasonable later cleanup and is not part of this change.

### Decision 2: Do not skip the blank line after the header

Only the lines from the opening to the closing marker are excluded. A blank line that follows still counts. Excluding it would mean guessing at layout, and one line against a 50-line budget is not worth a second rule.

### Decision 3: Unterminated header counts in full

If line 1 is `---` and no later line is exactly `---`, return 0. Markdown also uses `---` as a horizontal rule, and a hub that opens with a rule must not lose its whole body from the count.

### Decision 4: Message names the exclusion only when it applies

With no header the message is unchanged, so AGSZ-001 and AGSZ-002 keep passing as written. With a header the message adds ` excluding N front matter lines`.

```python
def front_matter_length(lines: list[str]) -> int:
    if not lines or lines[0].strip() != "---":
        return 0
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return i + 1
    return 0
```

## Risks

- A hub could hide content inside a long header. The header is machine-read metadata, not instructions, and the intent-book convention is two fields. If abuse appears, cap the excluded length rather than drop the exemption.
