# ASE Testing Convention

> Generic. Applicable to any project, any stack. Instantiate via `docs/testing-strategy.md`.

This is the invariant part of ASE testing. It defines what doesn't change across projects: the test layer taxonomy, the AC ID contract, the traceability model, and the proof requirements. `docs/testing-strategy.md` instantiates these for a specific project — choosing tools, CI wiring, and directory layout.

---

## Test Layers

Every acceptance criterion declares its required proof layer. The layer tells implementers and CI what kind of test proves the behavior. A scenario that says `**Test:** Unit` asks for fast pure-logic proof. A scenario that says `**Test:** E2E` asks for workflow-level evidence.

| Layer | Category | Purpose | Run |
|---|---|---|---|
| L1 | `Unit` | Pure logic, no I/O, no framework startup | Every push |
| L2 | `Slice` | Framework wiring, controllers, repositories, focused behavior | Every push |
| L3 | `Integration` | Real infrastructure contracts (DB, queues, APIs) | Every push or PR |
| L4 | `E2E` | Full workflows across service boundaries | PR and merge to main |
| L5 | `Performance` | Load, throughput, latency | On demand or scheduled |

> **Why Slice?** Unit tests isolate logic. Integration tests bring up real dependencies (database, queues, network). Slice tests sit between them — they wire up a vertical slice of the application (controller + serializer + validator, or repository + mapping layer) in a lightweight test context, without real I/O. Cheaper than integration, broader than unit.
>
> **Example:** Testing a checkout flow — apply a discount code, calculate the order total, and handle an expired code — with the real pricing engine and discount validator wired together, but a fake payment gateway. The slice proves the business logic wiring, not the bank integration.
>
> ISTQB calls this "component integration testing." If your framework doesn't support sliced test contexts (`@WebMvcTest`, `TestServer`, `supertest`), remove or rename this layer in your strategy.

### Supporting Categories

| Category | Purpose |
|---|---|
| `Baseline` | Structural or coverage-threshold-driven tests for code paths not linked to any AC. Provides regression protection without claiming product-behavior proof. |
| `Architectural` | Static or structural rules (dependency direction, layer boundaries) |
| `Manual` | Subjective or environment-specific checks that cannot reasonably be automated |
| `Sanity` | Toolchain and environment readiness checks |

A scenario without a declared test category is underspecified. A test without a declared category is unplaced.

---

## Acceptance Criteria (AC) IDs

Every scenario in a spec SHALL have a stable AC ID in `[PREFIX-NNN]` format:

```markdown
#### Scenario: Points earned on delivery [LP-001]

**Test:** Unit

- **GIVEN** an order has been marked as delivered
- **WHEN** the order total is at least $5.00
- **THEN** 1 point per dollar is awarded to the customer
```

Rules:
- IDs are unique within the project, zero-padded, sequential per prefix
- Once assigned, an ID SHALL NOT be reused or renumbered
- Removed scenarios keep their IDs in archive history — do not renumber remaining scenarios
- The prefix maps to the spec or capability name (e.g., `LP` for Loyalty Points, `DRAM` for DRAM module)

---

## Test Type Declaration

Every scenario SHALL declare its required test layer immediately after the heading:

```markdown
**Test:** Unit
**Test:** Integration
**Test:** Unit, Integration  # When multiple layers are required
```

If a scenario has no `**Test:**` field, the proof strategy is implicit — that is a spec quality gap.

---

## Positive and Negative Proof

Every non-Manual acceptance criterion SHALL be proven by tests that cover its significant equivalence classes and boundaries — both valid and invalid cases. A single positive test is not a proof strategy.

- **Positive proof**: The intended behavior works, including edge cases within valid boundaries.
- **Negative proof**: Invalid, forbidden, or boundary conditions fail as intended.

Proof coverage is guided by classical test design techniques (Equivalence Partitioning, Boundary Value Analysis). A scenario requiring only one positive and one negative test should be re-examined — it likely under-specifies the behavior or over-simplifies the proof.

---

## Traceability Markers

Tests that prove acceptance criteria SHALL carry a machine-readable marker linking back to the AC ID:

| Framework | Marker format |
|---|---|
| JUnit | `@Tag("LP-001")` |
| pytest | `@pytest.mark.ac("LP-001")` |
| Cucumber | `@AC:LP-001` |
| Go testing | `// AC: LP-001` |
| Fallback (any language) | `// AC: LP-001` |

Tests that do NOT prove acceptance criteria SHALL still declare what they are:

| Marker | Meaning |
|---|---|
| `@Tag("BASELINE")` | Coverage-threshold or structural regression protection |
| `@Tag("SANITY")` | Toolchain or environment readiness |
| `@Tag("ARCHITECTURAL")` | Structural rule enforcement |

A product-behavior test with no AC marker is a policy violation. If it proves externally visible behavior, the scenario should exist first.

---

## Task-Level Proof

In `tasks.md`, every production-code task SHALL be followed by explicit proof tasks when the behavior is testable.

Weak:
```markdown
- [ ] Add tests
```

Strong:
```markdown
- [ ] Add positive integration test for registered CISIC routing
  - Covers: DRAM-003
- [ ] Add negative integration test for unregistered CISIC rejection
  - Covers: DRAM-003
```

Proof tasks SHALL declare which AC IDs they cover via `Covers:` annotations.

---

## Verification Layers

ASE testing verification operates at three levels:

| Layer | What it does | Automation |
|---|---|---|
| **Registry** | Machine-generated map: every AC ID → spec source → test markers → coverage status. Read by humans and agents as a single source of traceability truth. | Deterministic |
| **Deterministic check** | Invalid ACs, missing coverage, orphaned markers — fails CI. Enforces the traceability contract mechanically. | Deterministic |
| **AC fidelity check** | AI review: does a tagged test actually prove its linked Gherkin, or has it drifted? A test can carry the right `@Tag` and still test the wrong thing. | AI-assisted |

The registry is the rendered output of the deterministic scan. When specs change, re-run the check and the registry updates. The fidelity check catches what static scanning cannot: a tagged test that is well-formed but unfaithful to its scenario.

---

## CI Enforcement

CI SHALL cross-reference spec scenarios against test markers and fail the build when:

- A non-Manual AC has no test coverage
- A test references an AC ID that does not exist
- A test references a removed or invalid AC
- A product-behavior test has no AC marker

The enforcement model distinguishes between **documented** (the rule exists in docs), **tool-supported** (a script exists), and **CI-enforced** (the build fails). Maturity honesty prevents process theatre — do not claim a control lives in CI if it only lives in documentation.

---

## Definition of Done

For spec-driven work, "done" means more than the task checkbox. The checkpoints are:

1. Every non-Manual AC has a linked test marker
2. Every covered AC has positive and negative proof
3. The relevant tests pass
4. CI traceability reports no blocking gaps
5. The completed change is archived so accepted behavior moves into canonical specs

---

## References

The techniques and taxonomies in this convention are grounded in established software engineering practice:

- **ISTQB Certified Tester Foundation Level** (CTFL v4.0) — the international standard for test levels, test types, and test design techniques. Defines the component → integration → system → acceptance test level hierarchy. This convention refines that hierarchy for spec-driven workflows, adding the industry-recognized `Slice` level (vertical-slice framework tests such as `@WebMvcTest`, `@DataJdbcTest`) between unit and integration.
- **The Art of Software Testing** — Myers, Glenford J., Badgett, Tom, Sandler, Corey (3rd ed., 2011, Wiley). The foundational text on black-box test design techniques including Equivalence Partitioning and Boundary Value Analysis.
- **Test Pyramid** — Martin Fowler (2012). *The Practical Test Pyramid*. [martinfowler.com/bliki/TestPyramid.html](https://martinfowler.com/bliki/TestPyramid.html)
- **Specification by Example** — Gojko Adzic (2011). Examples as a single source of truth for both specification and functional proof. Manning Publications.
- **BDD / Cucumber** — Examples as living documentation, automatically checked against system behavior. [cucumber.io/docs/bdd](https://cucumber.io/docs/bdd/)

*This document is the invariant. See `docs/testing-strategy.md` for the project-specific instantiation.*
