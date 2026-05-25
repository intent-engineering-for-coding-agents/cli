# secrets Specification

## Purpose

Scans common text files for credential patterns that should never appear in plaintext: private key headers, AWS access keys, and generic credential assignments. Intended as a pre-commit safety net.

## Requirements

### Requirement: Secret pattern detection

The checker SHALL scan all text files (selected by extension) in the repo for the following patterns:
- PEM private key header: `-----BEGIN` followed by an optional algorithm prefix and `PRIVATE KEY`
- AWS access key ID: the `AKIA` prefix followed by 16 uppercase alphanumeric characters
- Credential assignment: a `password`, `passwd`, `secret`, `api_key`, or `apikey` identifier assigned a quoted string value of 12 or more non-whitespace characters

Any match SHALL produce a FAIL result listing the file and pattern type.

#### Scenario: No secrets found [SECR-001]

Test-type: unit

- **WHEN** no scanned file contains any of the secret patterns
- **THEN** the result is `PASS`

#### Scenario: AWS access key detected [SECR-002]

Test-type: unit

- **WHEN** a file contains a string matching the AKIA + 16-char AWS key pattern
- **THEN** the result is `FAIL` with the filename in the message

#### Scenario: Private key marker detected [SECR-003]

Test-type: unit

- **WHEN** a file contains a PEM private key header line
- **THEN** the result is `FAIL` with the filename in the message

#### Scenario: Credential assignment detected [SECR-004]

Test-type: unit

- **WHEN** a file contains a credential identifier assigned a non-trivial quoted value (12+ chars)
- **THEN** the result is `FAIL` with the filename in the message

### Requirement: Skip non-project directories

The checker SHALL skip files whose path includes `.git`, `node_modules`, `.venv`, `venv`, `__pycache__`, or `.mypy_cache`.

#### Scenario: Files inside .git/ are not scanned [SECR-005]

Test-type: unit

- **WHEN** a file inside `.git/` matches a secret pattern and no other files match
- **THEN** the result is `PASS`

### Requirement: Checker registration

#### Scenario: Checker is registered [SECR-006]

Test-type: unit

- **WHEN** the checkers package is imported
- **THEN** `"secrets"` appears in `registry.list_all()`
