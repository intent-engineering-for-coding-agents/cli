# Design: docs-index-scope

## Context

Two existing checkers govern `INDEX.md`:

- `docs-index-exists` (DINE) — every `docs/` subdir SHOULD have one.
- `docs-index-stale` (DINS) — the listed entries SHOULD match the on-disk contents *of the directory the INDEX sits in*.

Both treat each INDEX as the agent-facing map of its own directory. Neither catches an INDEX that *expands its scope* — listing per-file entries from sub-directories or pointing to files outside `docs/` entirely. The new checker closes that gap.

## Goals / Non-Goals

**Goals:**
- Detect INDEX.md links that reach into a sub-directory's territory (deeper than one level), point to a parent path, or are absolute URLs.
- Allow same-directory file links and immediate sub-INDEX/README pointers — that is the entire shape of a well-formed flat INDEX.
- Reuse the link-parsing regex already proven by `docs-index-stale`.

**Non-Goals:**
- Validating *where* an absolute URL points or whether it 200s. The checker is about scope discipline, not link health.
- Validating linked filenames against on-disk reality (that is `docs-index-stale`'s job).
- Enforcing the shape of `README.md`. README is human prose; it can link wherever it wants.

## Decisions

### Decision 1: WARN severity, MEDIUM

**Chosen**: Status WARN, Severity MEDIUM — same as `docs-index-exists` and `docs-index-stale`.

**Rationale**: Scope drift is a discipline/style issue, not a missing artifact. It doesn't block agent boot; it pollutes the agent's mental model and creates rot. Symmetry with the other INDEX-focused checkers keeps the output legible.

### Decision 2: Match-only rule, no project-specific exceptions

**Chosen**: The rule is a closed-form regex. No allowlist, no config file, no "ignore these targets" escape hatch.

**Rationale**: Exceptions multiply. The rule is small enough that the fix is "move the link to README.md prose" — which is correct in every case observed so far (book repo's `../AGENTS.md` block is exactly this).

### Decision 3: Anchor fragments allowed

**Chosen**: A target whose text consists only of `#section` (or `a.md#section`) is treated as in scope. The checker strips `#fragment` before applying the rule.

**Rationale**: Same-page or same-file anchors are inert relative to scope. Forbidding them would force prose-style rewrites for no clarity gain.

### Decision 4: Shared link parser

**Chosen**: Move `_LINK_RE` from `docs_index_stale.py` to `checkers/_shared.py` and rename to `LINK_RE` (drop the leading underscore — it's now a public utility in a shared module). Both `docs_index_stale` and `docs_index_scope` import it.

**Rationale**: Same regex, same edge cases (text/path capture groups, no nested-paren support). Centralizing now prevents the two from drifting later. `_shared.py` already exists from the previous change and is the natural home.

### Decision 5: docs/ missing returns FAIL

**Chosen**: If `docs/` itself does not exist, FAIL (severity HIGH), matching the pattern in the other three docs checkers.

**Rationale**: Consistency. A missing `docs/` is an early-exit failure for all docs-* checkers.

## Risks / Trade-offs

- **[Trade-off]** The book repo's `docs/INDEX.md` will fire WARNs on the first run after this change is merged but before the book cleanup ships. Intentional and immediately fixed by the paired cleanup commit. The CI ordering note in the parent plan accepts one intermediate red.
- **[Risk]** A future legitimate cross-tree reference (e.g. linking to a peer book in a monorepo) would WARN. If/when that comes up, the response is to add an explicit exception scenario rather than weaken the rule by default.
- **[Risk]** The regex `LINK_RE` does not handle nested parentheses in URLs (`foo(bar)`). Already a limitation of `docs-index-stale`; accepted, not introduced here.
