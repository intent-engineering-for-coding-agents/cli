# checker-registry Specification

## Purpose
TBD - created by archiving change check. Update Purpose after archive.
## Requirements
### Requirement: Checker registration via decorator

The system SHALL provide a `@registry.register` decorator that adds a checker to the global registry. The decorator SHALL accept a class that conforms to the `Checker` protocol (has `id`, `description`, and `check(path: Path) -> CheckResult` attributes). Registration SHALL be idempotent — registering the same checker ID twice is a no-op.

#### Scenario: Register a checker [CHKREG-001]

Test-type: unit

- **WHEN** a checker class is decorated with `@registry.register`
- **THEN** the checker is added to the registry and discoverable by `registry.list_all()`

#### Scenario: Duplicate registration is idempotent [CHKREG-002]

Test-type: unit

- **WHEN** the same checker class is decorated twice (e.g., module re-import)
- **THEN** the registry contains exactly one instance of that checker

#### Scenario: Reject non-conforming registration [CHKREG-003]

Test-type: unit

- **WHEN** a class without `id` or `check` method is passed to `registry.register`
- **THEN** a `TypeError` is raised with a message identifying the missing attribute

### Requirement: Checker protocol definition

The system SHALL define a `Checker` protocol with three attributes: `id` (str, unique identifier), `description` (str, one-line summary), and `check(path: Path) -> CheckResult` (method accepting a repo root path and returning a result).

#### Scenario: Protocol conformance [CHKREG-004]

Test-type: unit

- **WHEN** a class has `id: str`, `description: str`, and `check(self, path: Path) -> CheckResult`
- **THEN** the class satisfies the `Checker` protocol without explicit inheritance

### Requirement: Run all registered checkers

The registry SHALL provide a `run_all(path: Path)` method that executes every registered checker against the given path and returns a list of `CheckResult` objects. Checkers SHALL run in registration order. A failure in one checker SHALL NOT prevent subsequent checkers from running.

#### Scenario: Run all checkers successfully [CHKREG-005]

Test-type: unit

- **WHEN** `registry.run_all(path)` is called with 3 registered checkers that all pass
- **THEN** a list of 3 `CheckResult` objects with `PASS` status is returned

#### Scenario: One checker fails, others continue [CHKREG-006]

Test-type: unit

- **WHEN** `registry.run_all(path)` is called and the second checker returns `FAIL`
- **THEN** the third checker still runs and its result is included in the returned list

#### Scenario: Checker raises unexpected exception [CHKREG-007]

Test-type: unit

- **WHEN** a checker raises an unexpected exception during `run_all`
- **THEN** a `CheckResult` with status `FAIL` and the exception message is included for that checker, and remaining checkers still run

#### Scenario: Empty registry [CHKREG-008]

Test-type: unit

- **WHEN** `registry.run_all(path)` is called with no registered checkers
- **THEN** an empty list is returned (not an error)

### Requirement: Run a single checker by ID

The registry SHALL provide a `run_one(check_id: str, path: Path)` method that executes a single checker by its unique ID.

#### Scenario: Run existing checker [CHKREG-009]

Test-type: unit

- **WHEN** `registry.run_one("agents-exists", path)` is called
- **THEN** only the checker with ID "agents-exists" executes and its result is returned

#### Scenario: Run non-existent checker [CHKREG-010]

Test-type: unit

- **WHEN** `registry.run_one("nonexistent", path)` is called
- **THEN** a `KeyError` is raised with the unknown checker ID in the message

### Requirement: List all registered checker IDs

The registry SHALL provide a `list_all()` method that returns a list of `(id, description)` tuples for all registered checkers, in registration order.

#### Scenario: List checkers [CHKREG-011]

Test-type: unit

- **WHEN** 3 checkers are registered with IDs "a", "b", "c"
- **THEN** `registry.list_all()` returns `[("a", "..."), ("b", "..."), ("c", "...")]`

