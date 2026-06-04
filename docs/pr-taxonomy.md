# PR Taxonomy

`iec-cli` follows a three-type PR taxonomy that maps directly to the OpenSpec two-PR model and to the CI gate set applied to each PR.

## The three types

### `docs`

Documentation-only changes. No code, no spec files, no tasks.

Examples: README edits, CONTRIBUTING updates, `docs/` prose changes, typo fixes.

CI gates: lint only. `iec check` is advisory — the gate logic in `tasks-complete` and `change-archived` does not apply because no change folder is touched.

### `structural`

Spec, ADR, design, or task-list changes with no implementation code. This is the **spec PR** half of the OpenSpec two-PR model.

Examples: new change folder under `openspec/changes/<name>/`, new ADR, new design doc.

CI gates: lint, `spec-ac-ids`, `spec-test-category`, `adr-format`, `adr-index`. The `tasks-complete` check does not yet apply (tasks are defined, not complete). `change-archived` does not apply (the change is not finished).

### `behavior`

Implementation changes that alter observable behaviour. This is the **implementation PR** half of the OpenSpec two-PR model. Requires an approved structural PR first.

Examples: new checker, bug fix, CLI flag change, refactored module.

CI gates: lint, test, `test-traceability`, `tasks-complete` (all spec tasks must be checked off before the implementation PR merges), `secrets`, all ci-enforced structure checks.

After the `behavior` PR merges to trunk: `change-archived` triggers on the next `iec check` run until the change folder is archived.

## Why this taxonomy

The taxonomy makes the spec-before-implementation discipline visible at the PR level. Reviewers know at a glance whether they are reviewing intent (structural) or execution (behavior). CI gates are scoped accordingly — the `tasks-complete` gate on behavior PRs is the mechanical enforcement of "no code without a spec".

See also: [docs/checks.md](checks.md) for the full check catalogue and maturity labels.

## PR title conventions

Prefix the PR title with the type in brackets:

```
[docs]       Fix typo in contributing guide
[structural] Spec: add docs-index-scope checker (change 012)
[behavior]   Implement docs-index-scope checker
```

This convention feeds the PR taxonomy check (`branch-matches-slug`, a future planned addition) and makes the changelog easier to generate.
