# eval-cli Specification

## Purpose

`ase eval` runs a YAML-driven eval suite against a repo state and prints a score table. Each eval task is a directory with a `checks.yaml` defining structural property checks. The command is used to detect regressions in agent output across AGENTS.md changes.

## Requirements

### Requirement: Task discovery

`ase eval` discovers tasks by walking the eval directory, sorted alphabetically, filtering to subdirectories that contain `checks.yaml`.

#### Scenario: No eval tasks found [EVAL-001]

Test-type: integration

- **WHEN** `--eval-dir` points to a directory with no task subdirectories
- **THEN** output contains "No eval tasks found" and exit code is 0

### Requirement: file_exists check type

#### Scenario: file_exists PASS [EVAL-008]

Test-type: unit

- **WHEN** a `file_exists` check is run and the path exists
- **THEN** result status is PASS

#### Scenario: file_exists with glob pattern [EVAL-008]

Test-type: unit

- **WHEN** a `file_exists` check uses a glob pattern like `docs/*.md`
- **THEN** PASS if any file matches, FAIL if none

### Requirement: file_contains check type

#### Scenario: file_contains PASS [EVAL-005]

Test-type: unit

- **WHEN** the file exists and the pattern matches
- **THEN** result status is PASS

#### Scenario: file_contains FAIL [EVAL-006]

Test-type: unit

- **WHEN** the file exists and the pattern does not match
- **THEN** result status is FAIL with the file name in the message

#### Scenario: file_contains uses MULTILINE [EVAL-005]

Test-type: unit

- **WHEN** the pattern contains `^` and the match is not at the start of the file
- **THEN** `^` anchors to line starts, not the start of the file

#### Scenario: file_contains missing file [EVAL-005]

Test-type: unit

- **WHEN** the target file does not exist
- **THEN** result status is FAIL with "not found" in the message

### Requirement: file_not_contains check type

#### Scenario: file_not_contains PASS and FAIL [EVAL-007]

Test-type: unit

- **WHEN** `file_not_contains` check is run
- **THEN** PASS if pattern absent, FAIL if pattern present

### Requirement: directory_exists check type

#### Scenario: directory_exists PASS and FAIL [EVAL-009]

Test-type: unit

- **WHEN** `directory_exists` check is run
- **THEN** PASS if directory exists, FAIL otherwise

### Requirement: Malformed YAML handling

#### Scenario: Malformed checks.yaml produces FAIL [EVAL-010]

Test-type: unit, integration

- **WHEN** a `checks.yaml` file cannot be parsed
- **THEN** the task produces a single FAIL result with "parse error" in the message

### Requirement: CLI flags

#### Scenario: --eval-dir flag [EVAL-011]

Test-type: integration

- **WHEN** `--eval-dir` points to a custom directory
- **THEN** tasks are loaded from that directory

#### Scenario: --path flag [EVAL-012]

Test-type: integration

- **WHEN** `--path` points to a custom repo root
- **THEN** all file checks are scoped to that root

### Requirement: Severity default

#### Scenario: Severity defaults to HIGH [EVAL-013]

Test-type: unit

- **WHEN** a check has no `severity` field in `checks.yaml`
- **THEN** the result uses Severity.HIGH

### Requirement: Exit codes

#### Scenario: All pass exits 0 [EVAL-014]

Test-type: integration

- **WHEN** all checks pass
- **THEN** exit code is 0 and score shows 100%

#### Scenario: Warnings only exits 1 [EVAL-015]

Test-type: integration

- **WHEN** only warnings exist (no failures)
- **THEN** exit code is 1

#### Scenario: Failures exit 2 [EVAL-016]

Test-type: integration

- **WHEN** at least one check fails
- **THEN** exit code is 2 and the Failures block is printed

### Requirement: Help registration

#### Scenario: ase --help lists eval [EVAL-017]

Test-type: integration

- **WHEN** `ase --help` is run
- **THEN** `eval` appears in the command list

### Requirement: Score output

#### Scenario: All pass, score line [EVAL-002]

Test-type: integration

- **WHEN** all checks pass
- **THEN** score line shows `X/X (100%)`

#### Scenario: Mixed results, table counts [EVAL-004]

Test-type: integration

- **WHEN** some checks pass and some fail
- **THEN** the table shows correct Pass/Warn/Fail counts per task

#### Scenario: One failure, failures block [EVAL-003]

Test-type: integration

- **WHEN** one check fails
- **THEN** exit code is 2 and the failure appears in the Failures block
