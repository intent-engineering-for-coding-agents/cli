# Proposal: Agent Hub Structure and Secrets Checks

## Why

The `.agents/` hub is the single source of truth for agent instructions. Without `instructions/` and `skills/` subdirectories, the hub is incomplete and agents fall back to guessing. The `secrets` check catches the most common class of credential exposure before it reaches a commit — private keys, AWS access keys, and password assignments with non-trivial values.

## What Changes

- **`agents-hub-structure` checker**: Verifies `.agents/` exists and has both `instructions/` and `skills/` subdirectories. FAIL if any are missing.
- **`secrets` checker**: Scans common text file types for private key markers, AWS access keys, and generic credential assignments. Skips `.git/`, `node_modules/`, `.venv/`, and `__pycache__/`. FAIL if any pattern is found.

## Capabilities

### New Capabilities

- `agents-hub-structure`: Checks `.agents/` structure. FAIL if `.agents/` is missing or either required subdirectory is absent.
- `secrets`: Scans text files for credential patterns. FAIL on first match per file.

### Modified Capabilities

*(None)*

## Impact

- **New modules**: `src/iec_cli/checkers/agents_hub_structure.py`, `src/iec_cli/checkers/secrets.py`
- **Updated**: `src/iec_cli/checkers/__init__.py`
- **Tests**: 12 unit tests (AHUB-001..006, SECR-001..006)
- **No new dependencies**
