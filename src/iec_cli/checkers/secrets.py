"""secrets — scan for secrets and credentials in plaintext files."""

import re
from pathlib import Path

from iec_cli.check import CheckResult, Maturity, Severity, Status, registry

_SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache"}

_TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".json",
    ".env",
    ".sh",
    ".bash",
    ".zsh",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".rb",
    ".go",
    ".java",
    ".cs",
    ".rs",
    ".php",
    ".pem",
    ".key",
    ".cert",
    ".crt",
}

_SECRET_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY"),
        "private key marker",
    ),
    (
        re.compile(r"AKIA[0-9A-Z]{16}"),
        "AWS access key",
    ),
    (
        re.compile(
            r'(?i)(?:password|passwd|secret|api_key|apikey)\s*=\s*["\'][^"\'<>{}\s]{12,}["\']'
        ),
        "credential assignment",
    ),
]


def _text_files(path: Path) -> list[Path]:
    files: list[Path] = []
    for entry in path.rglob("*"):
        if entry.is_file() and entry.suffix.lower() in _TEXT_EXTENSIONS:
            if not any(part in _SKIP_DIRS for part in entry.parts):
                files.append(entry)
    return sorted(files)


def _scan_file(filepath: Path, path: Path) -> list[str]:
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    rel = filepath.relative_to(path)
    return [
        f"{rel}: {label} detected"
        for pattern, label in _SECRET_PATTERNS
        if pattern.search(content)
    ]


@registry.register
class Secrets:
    id = "secrets"
    maturity = Maturity.CI
    description = "Scan for secrets and credentials in plaintext files"

    def check(self, path: Path) -> CheckResult:
        violations: list[str] = []
        for text_file in _text_files(path):
            violations.extend(_scan_file(text_file, path))

        if not violations:
            return CheckResult(
                self.id, Status.PASS, "No secrets detected", Severity.HIGH
            )
        return CheckResult(
            self.id,
            Status.FAIL,
            f"{len(violations)} potential secret(s): {'; '.join(violations)}",
            Severity.HIGH,
        )
