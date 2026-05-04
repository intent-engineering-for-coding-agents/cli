# docs/ — Agent-Facing Index

Every file in `docs/` listed with its purpose. Load this first for context economy.

## Root

| File | Purpose |
|---|---|
| [README.md](README.md) | Architecture overview — CLI design, two-layer checks, technology stack, command reference |
| INDEX.md | This file — agent-facing map, loaded first |

## decisions/ — Architectural Decision Records (MADR)

Permanent. Immutable once closed. Each records a real architectural decision made during ase-cli development.

| File | Purpose |
|---|---|
| [0001-python-typer.md](decisions/0001-python-typer.md) | Why Python + Typer for the CLI |
| [0002-canonical-docs-dir.md](decisions/0002-canonical-docs-dir.md) | Why `docs/` is the canonical documentation directory |
| [0003-two-layer-checks.md](decisions/0003-two-layer-checks.md) | Why deterministic + MCP for AI checks |
| [0004-byok-mcp.md](decisions/0004-byok-mcp.md) | Why BYOK via MCP, not direct API calls |
| [0005-madr-format.md](decisions/0005-madr-format.md) | Why MADR format for all ADRs |
| [0006-openspec.md](decisions/0006-openspec.md) | Why OpenSpec for spec-driven development |
| [README.md](decisions/README.md) | Auto-rendered listing of all ADRs with status |

## design/ — Feature Design Docs

Temporary. Per-feature. Disposable after implementation.

| File | Purpose |
|---|---|
| [README.md](design/README.md) | Auto-rendered listing of all design docs |
