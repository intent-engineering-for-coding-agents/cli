"""ase init — scaffold ASE canonical directory structure."""

# ruff: noqa: E501  # File ships verbatim Markdown content as string literals

from pathlib import Path

import typer

init_app = typer.Typer()

ASE_DIRS: list[str] = [
    "docs/architecture",
    "docs/decisions",
    "docs/design",
    "openspec/changes/archive",
    "openspec/specs",
    ".agents/instructions",
    ".agents/commands",
    ".agents/skills",
    ".agents/hooks",
]

GITKEEP_DIRS: set[str] = {
    "docs/architecture",
    "openspec/changes/archive",
    "openspec/specs",
    ".agents/instructions",
    ".agents/commands",
    ".agents/skills",
    ".agents/hooks",
}

AGENTS_TEMPLATE: str = """\
# AGENTS.md — {name}

You are working on **{name}**.

## Project

- **Language**: <!-- e.g. Python, Java, TypeScript -->
- **Framework**: <!-- e.g. Typer, Spring Boot, Next.js -->
- **Package manager**: <!-- e.g. uv, Gradle, npm -->

## Instructions

Load when relevant:

- <!-- [Build and CI](.agents/instructions/build-and-ci.md) — Build commands, CI -->
- <!-- [Coding standards](.agents/instructions/coding-standards.md) — Style, conventions -->
- [docs/INDEX.md](docs/INDEX.md) — Full map of all documentation
"""

# fmt: off
TESTING_STRATEGY_STUB: str = """\
# {name} Testing Strategy

> Concrete instantiation of `docs/testing-convention.md` for this project.

---

## Applicable Test Layers

| Layer | Category | Applies? | What it means here |
|---|---|---|---|
| L1 | `Unit` | <!-- Yes/No --> | <!-- Describe unit test scope --> |
| L2 | `Slice` | <!-- Yes/No --> | <!-- Or remove if not applicable --> |
| L3 | `Integration` | <!-- Yes/No --> | <!-- Describe integration test scope --> |
| L4 | `E2E` | <!-- Yes/No --> | <!-- Describe E2E test scope --> |
| L5 | `Performance` | <!-- Yes/No --> | <!-- Describe performance test scope --> |

| Category | Applies? | What it means here |
|---|---|---|
| `Baseline` | <!-- Yes/No --> | <!-- Coverage-threshold tests --> |
| `Architectural` | <!-- Yes/No --> | <!-- Static/structural rule checks --> |
| `Manual` | <!-- Yes/No --> | <!-- Manual verification steps --> |
| `Sanity` | <!-- Yes/No --> | <!-- Environment/toolchain checks --> |

---

## AC ID Format

Prefixes map to capability names in `openspec/specs/<capability>/`:

| Capability | Prefix |
|---|---|
| <!-- <capability-name> --> | <!-- <PREFIX> --> |

---

## Traceability Markers

<!-- Define language-specific markers, e.g. @pytest.mark.ac("PREFIX-NNN") -->

---

## Test Directory Layout

```
tests/
<!-- Define directory structure -->
```

---

## CI Wiring

<!-- Define CI workflow and test commands -->

---

## Maturity

| Layer | Maturity |
|---|---|
| <!-- L1 Unit --> | <!-- Documented / Tool-supported / CI-enforced --> |

---

*Instantiates `docs/testing-convention.md`. Update this file when adding new test infrastructure, CI gates, or capability prefixes.*
"""

CLAUDE_CONTENT: str = """\
@AGENTS.md
"""

GEMINI_CONTENT: str = """\
{
  "context": {
    "fileName": "AGENTS.md"
  }
}
"""

DOCS_README_STUB: str = """\
# Architecture Overview

<!-- Describe the high-level architecture of this project. -->

## Technology Stack

<!-- Key technologies, frameworks, and tools. -->

## System Design

<!-- Architecture diagrams, system boundaries, data flow. -->

## Key Decisions

<!-- Link to ADRs in docs/decisions/ for detailed decision records. -->
"""

DOCS_DECISIONS_README: str = """\
# Architectural Decision Records

| ADR | Title | Status |
|---|---|---|
<!-- | [0001-example.md](0001-example.md) | Example decision | Proposed | -->
"""

DOCS_DESIGN_README: str = """\
# Design Docs

| Design Doc | Feature |
|---|---|
<!-- | [example-feature.md](example-feature.md) | Example feature | -->
"""


def resolve_target(path: Path | None) -> Path:
    """Resolve target directory from --path flag or current working directory."""
    if path is None:
        return Path.cwd()
    target = Path(path).resolve()
    target.mkdir(parents=True, exist_ok=True)
    return target


def scaffold_dirs(target: Path, dry_run: bool = False) -> tuple[list[str], list[str]]:
    """Create all ASE canonical directories. Returns (created_dirs, created_gitkeeps)."""
    created_dirs: list[str] = []
    created_gitkeeps: list[str] = []
    for dirpath in ASE_DIRS:
        full = target / dirpath
        if not full.exists():
            if not dry_run:
                full.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(dirpath) + "/")
        # Place .gitkeep in directories that stay empty
        if dirpath in GITKEEP_DIRS:
            gitkeep = full / ".gitkeep"
            if not gitkeep.exists():
                if not dry_run:
                    gitkeep.touch()
                created_gitkeeps.append(str(dirpath) + "/.gitkeep")
    return created_dirs, created_gitkeeps


def scaffold_files(target: Path, force: bool = False, dry_run: bool = False) -> list[str]:
    """Create all ASE stub files. Returns list of created paths."""
    created: list[str] = []
    name = target.resolve().name

    files: dict[str, str] = {
        "AGENTS.md": AGENTS_TEMPLATE.format(name=name),
        "docs/README.md": DOCS_README_STUB,
        "docs/INDEX.md": _gen_index_stub(),
        "docs/testing-strategy.md": TESTING_STRATEGY_STUB.format(name=name),
        "docs/decisions/README.md": DOCS_DECISIONS_README,
        "docs/design/README.md": DOCS_DESIGN_README,
    }

    for relpath, content in files.items():
        full = target / relpath
        if full.exists() and not force:
            continue
        if not dry_run:
            full.write_text(content, encoding="utf-8")
        created.append(relpath)

    return created


def scaffold_testing_convention(target: Path, force: bool = False, dry_run: bool = False) -> str | None:
    """Create docs/testing-convention.md if missing (or forced). Returns path or None."""
    full = target / "docs" / "testing-convention.md"
    if full.exists() and not force:
        return None
    if dry_run:
        return "docs/testing-convention.md"
    content = _testing_convention_content()
    full.write_text(content, encoding="utf-8")
    return "docs/testing-convention.md"


def scaffold_vendor_files(
    target: Path,
    with_claude: bool = False,
    with_gemini: bool = False,
    force: bool = False,
    dry_run: bool = False,
) -> list[str]:
    """Create vendor pointer files. Returns list of created paths."""
    created: list[str] = []

    if with_claude:
        full = target / "CLAUDE.md"
        if not full.exists() or force:
            if not dry_run:
                full.write_text(CLAUDE_CONTENT, encoding="utf-8")
            created.append("CLAUDE.md")

    if with_gemini:
        full = target / ".gemini" / "settings.json"
        if not full.exists() or force:
            if not dry_run:
                full.parent.mkdir(parents=True, exist_ok=True)
                full.write_text(GEMINI_CONTENT, encoding="utf-8")
            created.append(".gemini/settings.json")

    return created


def report(
    created_dirs: list[str],
    created_gitkeeps: list[str],
    created_files: list[str],
    testing_convention: str | None,
    vendor_files: list[str],
    dry_run: bool = False,
) -> bool:
    """Print creation report. Returns True if any work was done."""
    action = "Would create" if dry_run else "Created"

    total = created_dirs + created_gitkeeps + created_files
    if testing_convention:
        total.append(testing_convention)
    total.extend(vendor_files)

    if not total:
        print("Already initialized. Nothing to do.")
        return False

    for d in created_dirs:
        print(f"  {action} directory: {d}")
    for g in created_gitkeeps:
        print(f"  {action} file: {g}")
    for f in created_files:
        print(f"  {action} file: {f}")
    if testing_convention:
        print(f"  {action} file: {testing_convention}")
    for v in vendor_files:
        print(f"  {action} file: {v}")

    return True


def _gen_index_stub() -> str:
    return """\
# docs/ — Agent-Facing Index

Every file in `docs/` listed with its purpose. Load this first for context economy.

## Root

| File | Purpose |
|---|---|
| [README.md](README.md) | Architecture overview |
| [testing-convention.md](testing-convention.md) | Generic ASE testing conventions |
| [testing-strategy.md](testing-strategy.md) | Project-specific test strategy |
| INDEX.md | This file — agent-facing map, loaded first |

## decisions/ — Architectural Decision Records (MADR)

| File | Purpose |
|---|---|
| [README.md](decisions/README.md) | Auto-rendered listing of all ADRs with status |

## design/ — Feature Design Docs

| File | Purpose |
|---|---|
| [README.md](design/README.md) | Auto-rendered listing of all design docs |
"""


def _testing_convention_content() -> str:
    return """\
# ASE Testing Convention

> Generic. Applicable to any project, any stack. Instantiate via `docs/testing-strategy.md`.

This is the invariant part of ASE testing. It defines what doesn't change across projects: the test layer taxonomy, the AC ID contract, the traceability model, and the proof requirements.

---

## Test Layers

| Layer | Category | Purpose | Run |
|---|---|---|---|
| L1 | `Unit` | Pure logic, no I/O, no framework startup | Every push |
| L2 | `Slice` | Framework wiring, controllers, repositories, focused behavior | Every push |
| L3 | `Integration` | Real infrastructure contracts (DB, queues, APIs) | Every push or PR |
| L4 | `E2E` | Full workflows across service boundaries | PR and merge to main |
| L5 | `Performance` | Load, throughput, latency | On demand or scheduled |

> **Why Slice?** Unit tests isolate logic. Integration tests bring up real dependencies. Slice tests sit between them — they wire up a vertical slice of the application in a lightweight test context, without real I/O. Cheaper than integration, broader than unit.
>
> **Example:** Testing a checkout flow — apply a discount code, calculate the order total, and handle an expired code — with the real pricing engine and discount validator wired together, but a fake payment gateway. The slice proves the business logic wiring, not the bank integration.
>
> ISTQB calls this "component integration testing." If your framework doesn't support sliced test contexts, remove or rename this layer in your strategy.

### Supporting Categories

| Category | Purpose |
|---|---|
| `Baseline` | Structural or coverage-threshold-driven tests for code paths not linked to any AC. Provides regression protection without claiming product-behavior proof. |
| `Architectural` | Static or structural rules (dependency direction, layer boundaries) |
| `Manual` | Subjective or environment-specific checks that cannot reasonably be automated |
| `Sanity` | Toolchain and environment readiness checks |

---

## Acceptance Criteria (AC) IDs

Every scenario in a spec SHALL have a stable AC ID in `[PREFIX-NNN]` format.

Rules:
- The prefix maps to the spec or capability name (e.g., `LP` for Loyalty Points)
- IDs are unique within the project, zero-padded, sequential per prefix
- Once assigned, an ID SHALL NOT be reused or renumbered
- Removed scenarios keep their IDs in archive history

---

## Test Type Declaration

Every scenario SHALL declare its required test layer immediately after the heading:

```markdown
**Test:** Unit
**Test:** Integration
**Test:** Unit, Integration
```

---

## Positive and Negative Proof

Every non-Manual acceptance criterion SHALL be proven by tests that cover its significant equivalence classes and boundaries — both valid and invalid cases. A single positive test is not a proof strategy.

---

## Traceability Markers

| Framework | Marker format |
|---|---|
| JUnit | `@Tag("LP-001")` |
| pytest | `@pytest.mark.ac("LP-001")` |
| Cucumber | `@AC:LP-001` |
| Go testing | `// AC: LP-001` |
| Fallback (any language) | `// AC: LP-001` |

Non-AC markers: `@Tag("BASELINE")`, `@Tag("SANITY")`, `@Tag("ARCHITECTURAL")`.

---

## Task-Level Proof

Proof tasks SHALL declare which AC IDs they cover via `Covers:` annotations.

---

## Verification Layers

| Layer | What it does | Automation |
|---|---|---|
| **Registry** | Machine-generated map: every AC ID → spec source → test markers → coverage status | Deterministic |
| **Deterministic check** | Invalid ACs, missing coverage, orphaned markers — fails CI | Deterministic |
| **AC fidelity check** | AI review: does a tagged test actually prove its linked Gherkin, or has it drifted? | AI-assisted |

---

## CI Enforcement

CI SHALL fail the build when:
- A non-Manual AC has no test coverage
- A test references an AC ID that does not exist
- A product-behavior test has no AC marker

The enforcement model distinguishes between **documented**, **tool-supported**, and **CI-enforced**.

---

## Definition of Done

1. Every non-Manual AC has a linked test marker
2. Every covered AC has positive and negative proof
3. The relevant tests pass
4. CI traceability reports no blocking gaps
5. The completed change is archived

---

## References

- **ISTQB Certified Tester Foundation Level** (CTFL v4.0) — test levels, test design techniques
- **The Art of Software Testing** — Myers et al. (3rd ed., 2011, Wiley) — Equivalence Partitioning, Boundary Value Analysis
- **Test Pyramid** — Martin Fowler (2012). [martinfowler.com/bliki/TestPyramid.html](https://martinfowler.com/bliki/TestPyramid.html)
- **Specification by Example** — Gojko Adzic (2011). Manning Publications
- **BDD / Cucumber** — [cucumber.io/docs/bdd](https://cucumber.io/docs/bdd/)

*This document is the invariant. See `docs/testing-strategy.md` for the project-specific instantiation.*
"""


@init_app.command()
def init(
    path: str | None = typer.Option(None, "--path", help="Target directory (default: current directory)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview what would be created"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files"),
    with_claude: bool = typer.Option(False, "--with-claude", help="Emit CLAUDE.md with @AGENTS.md import"),
    with_gemini: bool = typer.Option(
        False, "--with-gemini", help="Emit .gemini/settings.json pointing to AGENTS.md"
    ),
) -> None:
    """Scaffold the canonical ASE directory structure."""
    target = resolve_target(Path(path) if path else None)

    dirs, gitkeeps = scaffold_dirs(target, dry_run=dry_run)
    files = scaffold_files(target, force=force, dry_run=dry_run)
    tc = scaffold_testing_convention(target, force=force, dry_run=dry_run)
    vendor = scaffold_vendor_files(
        target, with_claude=with_claude, with_gemini=with_gemini, force=force, dry_run=dry_run
    )

    report(dirs, gitkeeps, files, tc, vendor, dry_run=dry_run)
