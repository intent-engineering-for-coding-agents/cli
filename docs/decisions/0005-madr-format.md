---
status: accepted
date: 2026-05-04
decision-makers: ASE Book Contributors
---

# ADR-0005: Use MADR Format for All Architectural Decision Records

## Context and Problem Statement

ASE practices require architectural decisions to be recorded in a permanent, structured format. The format must be plain text, version-controllable (Git-diffable), and machine-readable enough for deterministic validation. The book recommends a single ADR format — the tool must exemplify it.

## Considered Options

* MADR (Markdown Architectural Decision Records)
* Plain prose (unstructured Markdown)
* YAML-AD (YAML frontmatter + free text)
* Michael Nygard's original ADR format

## Decision Outcome

Chosen option: "MADR", because it is the most widely adopted structured plain-text ADR format. It requires a `Status` field (enabling deterministic validation of ADR state), a `Deciders` field, and structured sections (Context, Options, Decision, Consequences). MADR is plain Markdown — Git-diffable, GitHub-renderable, and simple enough that developers write ADRs rather than avoid them. The format aligns with ASE's plain-text-as-code principle.

### Consequences

* Good, because structured — mandatory sections enable deterministic validation (`ase check` can verify MADR compliance)
* Good, because plain Markdown — any editor, any Git host renders it
* Good, because widespread adoption — established community, templates available
* Good, because Michael Nygard's original format is a subset — MADR extends, does not break, it
* Bad, because more structured than plain prose — slightly higher barrier to writing (mitigated by the `adr-format` check in ase-cli itself, which validates template compliance)

## Pros and Cons of the Options

### MADR

* Good, because structured mandatory fields (`Status`, `Deciders`, `Date`)
* Good, because plain Markdown — no YAML, no JSON, no custom syntax
* Good, because GitHub renders it perfectly
* Good, because machine-validatable — deterministic checks can verify format compliance
* Good, because community-maintained template at adr.github.io/madr

### Plain prose

* Good, because zero barrier — write anything
* Bad, because unstructured — cannot validate, cannot auto-index reliably
* Bad, because inconsistent across authors — ADRs become free-form notes

### YAML-AD

* Good, because structured metadata in YAML frontmatter
* Bad, because YAML is error-prone (indentation sensitivity)
* Bad, because less common — fewer tools, fewer examples

### Michael Nygard's original ADR format

* Good, because simple — the original, minimal format
* Neutral, because MADR is a superset — adopting MADR does not conflict with Nygard's approach
* Neutral, because MADR adds structure (explicit sections, status field) without removing simplicity

## Validation

Verified by: ase-cli will include an `adr-format` deterministic check that validates all ADRs follow the MADR template. The tool dogfoods its own check — all ADRs in this repo pass `ase check --path docs/decisions/`.
