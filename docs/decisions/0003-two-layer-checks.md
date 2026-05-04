# ADR-0003: Two-Layer Check Architecture (Deterministic + MCP for AI)

* Status: accepted
* Deciders: ASE Book Contributors
* Date: 2026-05-04

## Context and Problem Statement

ase-cli validates ASE practices. Some checks are mechanical — file existence, size limits, format compliance — and can be validated with deterministic logic. Other checks are semantic — content quality, scope appropriateness — and require judgment. How should the tool structure these two categories of checks?

## Considered Options

* All deterministic — only mechanical checks, no semantic validation
* All AI-assisted — every check uses an AI model for evaluation
* Two-layer — deterministic checks in Python, semantic checks via MCP using user's AI

## Decision Outcome

Chosen option: "Two-layer", because mechanical checks should run instantly offline without AI dependency, while semantic checks benefit from AI judgment. The MCP protocol enables BYOK — the user brings their own AI agent, the tool doesn't manage API keys or model selection. This separation also makes the deterministic layer independently useful: anyone can run `ase check` without AI access.

### Consequences

* Good, because deterministic checks run instantly, offline, with zero AI cost
* Good, because AI-assisted checks handle what mechanical logic cannot (content quality, scope)
* Good, because BYOK via MCP means the tool never handles user API keys
* Good, because users can start with deterministic checks and add AI incrementally
* Bad, because two code paths (Python checks + MCP server) increase implementation complexity

## Pros and Cons of the Options

### All deterministic

* Good, because simple implementation — one code path
* Good, because no AI dependency, no MCP server complexity
* Bad, because cannot validate semantic quality (ADR scope creep, spec completeness, TOC quality)

### All AI-assisted

* Good, because unified code path
* Bad, because AI required for even trivial checks (file existence, format)
* Bad, because slower and costly for mechanical checks
* Bad, because AI hallucinations could produce false positives on mechanical checks

### Two-layer

* Good, because each layer handles what it does best
* Good, because incremental adoption — deterministic first, AI optional
* Good, because deterministic layer serves as fast-path for CI
* Neutral, because two code paths require a clear interface boundary — managed via plugin registry

## Validation

Verified by: deterministic check framework defined as plugin registry. MCP server defined as separate module. Both layers pass through a shared result format so `ase check` output is uniform regardless of check source.
