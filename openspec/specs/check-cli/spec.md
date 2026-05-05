# check-cli Specification

## Purpose
TBD - created by archiving change check. Update Purpose after archive.
## Requirements
### Requirement: ase check command

The system SHALL provide an `ase check` CLI command that runs all registered deterministic checkers. It SHALL accept an optional `--path` argument to scope checks to a specific directory (defaults to current working directory). It SHALL NOT accept `--all` or AI-related flags at this stage.

#### Scenario: Run checks with the default path [CHKCLI-001]

**Test:** Integration

- **WHEN** `ase check` is invoked without arguments
- **THEN** all registered checkers run against the current working directory and results are printed

#### Scenario: Run checks with explicit path [CHKCLI-002]

**Test:** Integration

- **WHEN** `ase check --path /some/repo` is invoked
- **THEN** all registered checkers run against `/some/repo`

#### Scenario: --help shows check command [CHKCLI-003]

**Test:** Integration

- **WHEN** `ase check --help` is invoked
- **THEN** the help text shows `--path` option with description

### Requirement: Human-readable summary output

The system SHALL print a human-readable summary after running all checks. The output SHALL include: total count of checks run, count of PASS/WARN/FAIL, and a per-checker line showing status and message. The output SHALL be plain text (no color codes).

#### Scenario: All checks pass [CHKCLI-004]

**Test:** Integration

- **WHEN** all registered checkers return `PASS`
- **THEN** the output shows each checker with `PASS`, a summary line "X check(s): X passed", and exit code 0

#### Scenario: One check fails [CHKCLI-005]

**Test:** Integration

- **WHEN** one checker returns `FAIL`
- **THEN** the output shows the failing checker with `FAIL` and its message, and a summary line reflecting the failure

#### Scenario: Mixed results [CHKCLI-006]

**Test:** Integration

- **WHEN** checkers return PASS, WARN, and FAIL
- **THEN** the summary shows all three counts and exit code 2 (failure)

### Requirement: Exit codes

The system SHALL exit with code 0 when all checks pass, code 1 when there are warnings but no failures, and code 2 when there are failures.

#### Scenario: Exit code 0 — all pass [CHKCLI-007]

**Test:** Integration

- **WHEN** all checkers return `PASS`
- **THEN** the process exits with code 0

#### Scenario: Exit code 1 — warnings only [CHKCLI-008]

**Test:** Integration

- **WHEN** at least one checker returns `WARN` and none return `FAIL`
- **THEN** the process exits with code 1

#### Scenario: Exit code 2 — failures present [CHKCLI-009]

**Test:** Integration

- **WHEN** at least one checker returns `FAIL` (regardless of warnings)
- **THEN** the process exits with code 2

### Requirement: Check ordering in output

The system SHALL display results in the same order checkers were registered in the registry.

#### Scenario: Output order matches registration order [CHKCLI-010]

**Test:** Unit

- **WHEN** checkers are registered with IDs "b", "a", "c"
- **THEN** the output lists results in order "b", "a", "c"

