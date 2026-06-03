---
status: accepted
date: 2026-05-04
decision-makers: ASE Book Contributors
---

# ADR-0001: Use Python with Typer for the CLI

## Context and Problem Statement

ase-cli needs a command-line interface for validating ASE practices. The tool must be easy to install and run on macOS, Linux, and Windows. Senior developers are the target audience. The language and framework choice affects install experience, development speed, ecosystem access, and alignment with ASE principles.

## Considered Options

* Python + Typer
* Node.js + Commander
* Go + Cobra
* Rust + Clap

## Decision Outcome

Chosen option: "Python + Typer", because Python is universal — pre-installed or trivially installed on all three target platforms — and Typer provides type-hint-driven CLI development with zero boilerplate. uv eliminates the historical Python packaging pain, making `uv tool install ase-cli` a single-step install comparable to Go or Rust. Python's readability aligns with the ASE principle of plain-text-as-code.

### Consequences

* Good, because Python is the most widely known language among the target audience (senior developers)
* Good, because Typer's type-hint-driven design reduces boilerplate and catches errors at development time
* Good, because uv makes Python distribution as simple as Go or Rust binaries
* Bad, because Python startup time is slower than compiled languages — acceptable for a validation CLI where checks are the bottleneck, not startup

## Pros and Cons of the Options

### Python + Typer

* Good, because universal platform support
* Good, because mature CLI ecosystem (Typer, Rich, Click)
* Good, because aligns with audience language familiarity
* Good, because uv solves packaging (single-command install)
* Neutral, because interpreted — slower startup, but checks dominate runtime

### Node.js + Commander

* Good, because widespread adoption, large ecosystem
* Bad, because requires Node.js runtime install — heavier than Python for many users
* Bad, because npm ecosystem churn creates maintenance burden
* Bad, because JavaScript/TypeScript type system is less expressive for CLI definition than Python type hints

### Go + Cobra

* Good, because single binary distribution — no runtime dependency
* Good, because fast startup and execution
* Bad, because smaller overlap with target audience (senior devs ≠ Go devs)
* Bad, because Go's error handling verbosity works against the plain-text readability principle

### Rust + Clap

* Good, because single binary, fast, memory-safe
* Bad, because steep learning curve reduces contributor pool
* Bad, because compile times slow iteration
* Bad, because over-engineered for a validation CLI — the bottleneck is I/O and model calls, not CPU

## Validation

Verified by: `uv tool install` flow tested on macOS, Linux, and Windows. Typer project scaffold confirmed working via CI (`uv sync && uv run ruff check . && uv run pytest`).
