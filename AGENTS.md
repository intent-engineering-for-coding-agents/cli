# AGENTS.md — ase-cli

You are working on **ase-cli**, a Python CLI that validates ASE practices.

## Project

- **Language**: Python 3.12+, type hints required
- **CLI framework**: Typer (type-hint-driven, no argparse)
- **Package manager**: uv (`uv sync --group dev`, `uv run`)
- **License**: Apache 2.0

## Instructions

Load when relevant:

- [Build and CI](.agents/instructions/build-and-ci.md) — uv commands, lint, test, CI pipeline
- [Coding standards](.agents/instructions/coding-standards.md) — Python style, project structure, testing
- [OpenSpec workflow](.agents/instructions/openspec.md) — Specs, AC IDs, test traceability
- [Index maintenance](.agents/instructions/index-maintenance.md) — When to update docs/INDEX.md
- [docs/INDEX.md](docs/INDEX.md) — Full map of all documentation

## Skills

- **update-index** — Scan `docs/`, regenerate `docs/INDEX.md` and all `docs/*/README.md` listing files
