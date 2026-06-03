# ase-cli Architecture

ase-cli is a Python CLI tool that validates ASE (Agentic Software Engineering) practices in any repository. It has two layers of checks: deterministic (runs without AI) and AI-assisted (via MCP, using the user's own AI).

## Design

```
┌──────────┐     ┌─────────────────┐     ┌──────────────┐
│   User   │────▶│  ase-cli (CLI)  │────▶│  Repo files  │
└──────────┘     └────────┬────────┘     └──────────────┘
                          │
                 ┌────────▼────────┐
                 │  Deterministic   │
                 │  checks (Python) │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │  MCP Server      │
                 │  (AI-assisted)   │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │  User's AI       │
                 │  Agent (BYOK)    │
                 └─────────────────┘
```

## Two-Layer Check Architecture

| Layer | Technology | What it checks |
|---|---|---|
| Deterministic | Pure Python | File size, structure, MADR format, AC ID patterns, test markers, secrets |
| AI-assisted | MCP server | Top-heavy content, ADR scope, AGENTS.md TOC quality, spec semantics |

The deterministic layer works on any machine — no AI required. The AI layer starts an MCP server. The user's AI agent connects and runs semantic checks. BYOK: the user brings their own AI.

## Commands

```
ase --help                # Show usage
ase --version             # Show version

ase init                  # Scaffold canonical ASE directory structure
ase init --path <dir>     # Target a specific directory
ase init --dry-run        # Preview what would be created
ase init --force           # Overwrite existing files
ase init --with-claude    # Also emit CLAUDE.md with @AGENTS.md import
ase init --with-gemini    # Also emit .gemini/settings.json context config

ase check                 # Run deterministic checks only (future)
ase check --all           # Run deterministic + AI-assisted (future)
ase check --path src/     # Scope to a directory or file (future)

ase generate              # Emit vendor agent instruction files (future)
```

## Technology Stack

| Concern | Choice | Why |
|---|---|---|
| Language | Python 3.12+ | Universal, readable, mature CLI ecosystem |
| CLI framework | Typer | Type-hint driven, fast to develop |
| Package manager | uv | Single tool for Python + packages |
| AI bridge | MCP (modelcontextprotocol.io) | BYOK, agent-agnostic |
| Lint/format | ruff | Fast, comprehensive |
| Test | pytest | Standard, well-supported |

## Repository Map

See [INDEX.md](INDEX.md) for the agent-facing map of all documentation.
