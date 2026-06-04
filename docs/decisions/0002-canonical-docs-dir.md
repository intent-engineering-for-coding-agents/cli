---
status: accepted
date: 2026-05-04
decision-makers: Intent Engineering for Coding Agents Contributors
---

# ADR-0002: Use `docs/` as Canonical Documentation Directory

## Context and Problem Statement

Intent Engineering practices recommend a canonical directory for architecture, decisions, and design documentation. The directory name must work across Git hosts (GitHub, GitLab, Bitbucket), static site generators, and programming language ecosystems without collision. It must be the single convention the book recommends.

## Considered Options

* `docs/`
* `doc/`
* `documentation/`
* `wiki/`

## Decision Outcome

Chosen option: "`docs/`", because GitHub, GitLab, and Bitbucket all render `README.md` from `docs/` automatically in their repository browsers. No common static site generator or framework claims `docs/` as its default output directory (unlike `doc/` which conflicts with Go, or `wiki/` which implies a wiki workflow). One name, one convention, no exceptions.

### Consequences

* Good, because GitHub/GitLab/Bitbucket automatically render `docs/README.md` in the repository file browser
* Good, because no tool collision — `docs/` is not claimed by any major framework as default output
* Good, because `docs/` is the de facto standard across open-source — readers expect it
* Good, because VitePress, Docusaurus, and mdBook can all point their source directory elsewhere, keeping `docs/` free for Intent Engineering documentation
* Bad, because some CI tools default to deploying from `docs/` (e.g., GitHub Pages legacy mode) — mitigated by using Actions-based deploy, not the built-in `/docs` deploy

## Pros and Cons of the Options

### docs/

* Good, because universal recognition — every developer knows what `docs/` means
* Good, because Git hosts render `README.md` from it automatically
* Good, because no framework claims it as default output
* Neutral, because slightly longer to type than `doc/`

### doc/

* Good, because shorter
* Bad, because Go ecosystem uses `doc/` for package documentation — collision risk
* Bad, because not as widely recognized as `docs/`

### documentation/

* Good, because explicit
* Bad, because verbose — violates the principle of keeping paths short for CLI usage
* Bad, because less common convention

### wiki/

* Bad, because implies a wiki workflow (user-editable, unstructured)
* Bad, because GitHub Wikis use a separate repo — naming collision

## Validation

Verified by: GitHub, GitLab, and Bitbucket all render `docs/README.md` in their repository file browsers. No framework in Intent Engineering's technology stack (VitePress, Typer, ruff, pytest, uv) claims `docs/` as default output.
