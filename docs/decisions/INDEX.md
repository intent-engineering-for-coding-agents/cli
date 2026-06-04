# docs/decisions/ — Agent-Facing Index

Every file in `docs/decisions/` listed with its purpose. Load this first for context economy.

## ADRs

| File | Purpose |
|---|---|
| [0001-python-typer.md](0001-python-typer.md) | Why Python + Typer for the CLI — readable, type-hint-driven, no argparse |
| [0002-canonical-docs-dir.md](0002-canonical-docs-dir.md) | Why `docs/` is the canonical documentation directory — one name that works everywhere |
| [0003-two-layer-checks.md](0003-two-layer-checks.md) | Why two-layer check architecture — deterministic (pure Python) + agent-assisted (MCP) |
| [0004-byok-mcp.md](0004-byok-mcp.md) | Why BYOK via MCP — user brings their own coding agent, tool doesn't care which one |
| [0005-madr-format.md](0005-madr-format.md) | Why MADR format for all architectural decisions — lightweight, structured, git-diffable |
| [0006-openspec.md](0006-openspec.md) | Why OpenSpec for spec-driven development — AC IDs, traceability, archive flow |
| [0007-ac-id-and-test-type-convention.md](0007-ac-id-and-test-type-convention.md) | Why `[PREFIX-NNN]` AC IDs and `Test-type:` field — machine-readable traceability |
| [README.md](README.md) | Auto-rendered listing of all ADRs with status |
