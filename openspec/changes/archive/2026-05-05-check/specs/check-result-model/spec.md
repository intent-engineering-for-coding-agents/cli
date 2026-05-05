# Check Result Model

The result model defines the structured output of every check: a status (pass/warn/fail), severity, message, optional source location, and optional AC ID for traceability.

## ADDED Requirements

### Requirement: Status enumeration

The system SHALL define a `Status` enum with three values: `PASS`, `WARN`, `FAIL`. `PASS` indicates the check found no issues. `WARN` indicates a minor issue that does not block CI. `FAIL` indicates an issue that should block CI.

#### Scenario: All status values defined [CHKRSL-001]

**Test:** Unit

- **WHEN** `Status` enum is imported
- **THEN** `Status.PASS`, `Status.WARN`, and `Status.FAIL` are available

### Requirement: Severity enumeration

The system SHALL define a `Severity` enum with three values: `HIGH`, `MEDIUM`, `LOW`. Severity indicates the importance of a finding, independent of pass/warn/fail status.

#### Scenario: All severity values defined [CHKRSL-002]

**Test:** Unit

- **WHEN** `Severity` enum is imported
- **THEN** `Severity.HIGH`, `Severity.MEDIUM`, and `Severity.LOW` are available

### Requirement: CheckResult dataclass

The system SHALL define a `CheckResult` dataclass with fields: `check_id` (str), `status` (Status), `message` (str), `severity` (Severity), `location` (str | None, defaults to None), and `ac_id` (str | None, defaults to None).

#### Scenario: Create a pass result with all fields [CHKRSL-003]

**Test:** Unit

- **WHEN** `CheckResult(check_id="agents-exists", status=Status.PASS, message="AGENTS.md found", severity=Severity.HIGH, location="AGENTS.md", ac_id="CHKRSL-003")` is constructed
- **THEN** all fields are set as given and `location` and `ac_id` are populated

#### Scenario: Create a fail result with minimal fields [CHKRSL-004]

**Test:** Unit

- **WHEN** `CheckResult(check_id="adr-format", status=Status.FAIL, message="Not MADR", severity=Severity.HIGH)` is constructed
- **THEN** `location` and `ac_id` default to `None`

#### Scenario: Result equality comparison [CHKRSL-005]

**Test:** Unit

- **WHEN** two `CheckResult` instances have identical field values
- **THEN** `==` returns `True`

### Requirement: CheckResult is_warning and is_failure helpers

`CheckResult` SHALL provide `is_warning` and `is_failure` properties that return `True` when status is `WARN` or `FAIL` respectively.

#### Scenario: is_warning property [CHKRSL-006]

**Test:** Unit

- **WHEN** a `CheckResult` has status `WARN`
- **THEN** `result.is_warning` returns `True` and `result.is_failure` returns `False`

#### Scenario: is_failure property [CHKRSL-007]

**Test:** Unit

- **WHEN** a `CheckResult` has status `FAIL`
- **THEN** `result.is_failure` returns `True` and `result.is_warning` returns `False`
