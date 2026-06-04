---
status: accepted
date: 2026-05-04
decision-makers: Intent Engineering for Coding Agents Contributors
---

# ADR-0006: Use OpenSpec for Spec-Driven Development

## Context and Problem Statement

Intent Engineering practices require a spec-driven development workflow. Specs capture intent before implementation, produce acceptance criteria with traceable IDs, and survive the implementation they guided. The spec format and tooling must be lightweight (plain text, Git-native), support brownfield codebases, and work across coding agents. The book must recommend one spec approach.

## Considered Options

* OpenSpec (openspec.dev)
* GitHub SpecKit
* LeanSpec (lean-spec.dev) — lightweight spec format only, no tooling
* Raw Markdown specs with no formal framework

## Decision Outcome

Chosen option: "OpenSpec", because it is the only option that is lightweight (no API keys, no MCP dependency, no vendor lock-in), universal (supports all major coding agents natively), and provides both a spec format and a CLI tool for managing spec lifecycles. Its directory structure maps directly to the canonical Intent Engineering layout. It works on brownfield codebases — specs are created incrementally as changes are proposed.

### Consequences

* Good, because specs are plain Markdown — Git-diffable, readable by any agent, no proprietary format
* Good, because AC IDs are part of the spec format — enables deterministic traceability checks in iec-cli
* Good, because `openspec/` directory maps to the Intent Engineering canonical structure (specs/ for current, changes/ for proposals)
* Good, because natively supported by the coding agents the book's audience uses (Claude Code, Codex, Cursor, Copilot, OpenCode, Windsurf)
* Good, because no API keys needed — the `openspec` CLI works locally
* Neutral, because the `openspec` CLI is distributed via npm — an additional tool install for readers using Python/uv. Mitigated by iec-cli providing its own spec validation layer, so npm is only needed for spec authoring, not validation

## How OpenSpec Fits With iec-cli

OpenSpec handles **spec authoring and lifecycle** — creating proposals, spec deltas, task breakdowns. The `openspec` CLI generates the directory structure and template files.

iec-cli handles **spec validation** — verifying that specs have AC IDs, test categories, size limits, and test traceability. iec-cli reads OpenSpec-formatted specs and validates them deterministically.

The two tools are complementary, not overlapping:
- `openspec` → writes specs (authoring)
- `iec-cli` → validates specs (quality)

## Pros and Cons of the Options

### OpenSpec

* Good, because lightweight — plain Markdown, no API keys, no MCP
* Good, because universal — works with all major coding agents
* Good, because brownfield-first — specs created incrementally, not all upfront
* Good, because structured — proposal, design, tasks, spec deltas in a known directory layout
* Good, because open source with an active community
* Neutral, because distributed via npm — not the Python ecosystem the book uses (but the spec format itself has no language dependency)

### GitHub SpecKit

* Good, because GitHub-native, enterprise-grade
* Bad, because heavier — more process, more upfront investment
* Bad, because less suited for individual developers and small teams (the book's primary audience)

### LeanSpec

* Good, because minimal — under 300 lines, important stuff first
* Good, because plain Markdown, no tooling required
* Bad, because no CLI — spec lifecycle management is manual
* Bad, because no standard for AC IDs — traceability is ad-hoc

### Raw Markdown specs

* Good, because zero tooling dependency
* Bad, because no structure enforcement — inconsistency across repos and teams
* Bad, because no spec delta mechanism — harder to review what changed in requirements

## Validation

Verified by: iec-cli's deterministic spec checks (`spec-ac-ids`, `spec-test-category`, `spec-size`) are designed to validate OpenSpec-formatted specs. The `openspec/` directory is part of the Intent Engineering canonical structure.
