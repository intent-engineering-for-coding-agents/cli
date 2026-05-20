# Design: Agent Hub Structure and Secrets Checks

## agents-hub-structure

Three `is_dir()` checks: `path / ".agents"`, `path / ".agents" / "instructions"`, `path / ".agents" / "skills"`. Collect missing items, report in a single FAIL. Returns PASS only if all three exist.

## secrets

Three regex patterns compiled at module load:
1. `-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY` — PEM private key header
2. `AKIA[0-9A-Z]{16}` — AWS access key (20-char format)
3. `(?i)(?:password|passwd|secret|api_key|apikey)\s*=\s*["\'][^"\'<>{}\s]{12,}["\']` — credential assignment with non-trivial value (12+ chars)

File discovery: walk `path.rglob("*")`, check `suffix.lower()` against an allow-list of text extensions (`.py`, `.js`, `.ts`, `.md`, `.yml`, `.yaml`, `.json`, `.env`, `.sh`, `.toml`, `.ini`, `.cfg`, `.conf`, `.rb`, `.go`, `.java`, `.cs`, `.rs`, `.php`, `.pem`, `.key`, `.cert`, `.crt`). Skip dirs in `{".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache"}`.

All three patterns are applied to each file. Multiple matches in one file produce multiple violation entries. `errors="ignore"` on read handles non-UTF-8 binary files that sneak through extension matching.

## Severity

Both checks: `Severity.HIGH`. Missing hub structure blocks agent context loading. Secret exposure is a security incident.
