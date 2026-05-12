"""adr-format — validate MADR filename, heading, required sections, and status."""

import re
from pathlib import Path

from ase_cli.check import CheckResult, Severity, Status, registry

_FILENAME_RE = re.compile(r"^\d{4}-[a-z0-9-]+\.md$")
_NUMBERED_HEADING_RE = re.compile(r"^# ADR-(\d{4}):")
_VALID_STATUS_PREFIXES = ("accepted", "deprecated", "superseded", "proposed")
_SKIP = {"README.md", "INDEX.md"}


def _parse_front_matter(lines: list[str]) -> tuple[dict[str, str], list[str]]:
    """Return (front_matter_dict, body_lines). Empty dict if no front matter."""
    if not lines or lines[0].strip() != "---":
        return {}, lines
    end = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end = i
            break
    if end == -1:
        return {}, lines
    fm: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip().lower()] = val.strip()
    return fm, lines[end + 1 :]


def _check_adr(filepath: Path) -> list[str]:
    """Return violation messages for one ADR file."""
    violations: list[str] = []
    name = filepath.name

    if not _FILENAME_RE.match(name):
        return [f"{name}: filename does not match NNNN-kebab-case.md pattern"]

    prefix = name[:4]
    lines = filepath.read_text(encoding="utf-8").splitlines()
    fm, body_lines = _parse_front_matter(lines)
    full_text = "\n".join(lines)

    # Title heading — look in body (after front matter) or full text for bullet style
    search_lines = body_lines if fm else lines
    first_heading: str | None = None
    for line in search_lines:
        stripped = line.strip()
        if stripped:
            if stripped.startswith("# "):
                first_heading = stripped
            break

    if first_heading is None:
        violations.append(f"{name}: missing # title heading")
    else:
        m = _NUMBERED_HEADING_RE.match(first_heading)
        if m and m.group(1) != prefix:
            violations.append(
                f"{name}: ADR number in heading ({m.group(1)}) "
                f"does not match filename prefix ({prefix})"
            )

    # Required sections
    if "## Context and Problem Statement" not in full_text:
        violations.append(f"{name}: missing '## Context and Problem Statement'")
    if "## Decision Outcome" not in full_text:
        violations.append(f"{name}: missing '## Decision Outcome'")

    # Status — YAML front matter takes precedence, then bullet style
    status_value: str | None = fm.get("status")
    if status_value is None:
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("* Status:"):
                status_value = stripped[len("* Status:") :].strip()
                break

    if status_value is None:
        violations.append(
            f"{name}: missing status (no YAML 'status:' or '* Status:' line)"
        )
    elif not any(status_value.startswith(p) for p in _VALID_STATUS_PREFIXES):
        violations.append(
            f"{name}: invalid status '{status_value}' "
            f"(must start with: {', '.join(_VALID_STATUS_PREFIXES)})"
        )

    return violations


@registry.register
class AdrFormat:
    id = "adr-format"
    description = "Validate ADR filenames, headings, required sections, and status"

    def check(self, path: Path) -> CheckResult:
        decisions_dir = path / "docs" / "decisions"
        if not decisions_dir.is_dir():
            return CheckResult(
                self.id, Status.PASS, "No docs/decisions/ directory", Severity.HIGH
            )

        adr_files = sorted(
            f
            for f in decisions_dir.iterdir()
            if f.is_file() and f.suffix == ".md" and f.name not in _SKIP
        )

        if not adr_files:
            return CheckResult(
                self.id, Status.PASS, "No ADR files to validate", Severity.HIGH
            )

        violations: list[str] = []
        for adr_file in adr_files:
            violations.extend(_check_adr(adr_file))

        if not violations:
            return CheckResult(
                self.id, Status.PASS, "All ADRs pass format checks", Severity.HIGH
            )
        return CheckResult(self.id, Status.FAIL, "; ".join(violations), Severity.HIGH)
