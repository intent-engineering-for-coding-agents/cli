"""Integration tests for the `iec check` CLI command."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from iec_cli.check import (
    CheckResult,
    Severity,
    Status,
    check_app,
    registry,
)

runner = CliRunner()


class _Pass:
    id = "a-ok"
    description = "Always passes"

    def check(self, path: Path) -> CheckResult:
        return CheckResult(self.id, Status.PASS, "all good", Severity.HIGH)


class _Warn:
    id = "b-caution"
    description = "Always warns"

    def check(self, path: Path) -> CheckResult:
        return CheckResult(self.id, Status.WARN, "be careful", Severity.MEDIUM)


class _Fail:
    id = "c-bad"
    description = "Always fails"

    def check(self, path: Path) -> CheckResult:
        return CheckResult(self.id, Status.FAIL, "something wrong", Severity.HIGH)


@pytest.fixture(autouse=True)
def _clean_registry() -> None:
    """Reset module-level registry before each test."""
    registry._checkers.clear()


# ---------------------------------------------------------------------------
# 4.1 / 4.2 — CLI entry points
# ---------------------------------------------------------------------------


def test_check_default_path() -> None:
    """Covers: CHKCLI-001"""
    registry.register(_Pass())
    result = runner.invoke(check_app)
    assert result.exit_code == 0
    assert "a-ok" in result.stdout
    assert "all good" in result.stdout


def test_check_explicit_path() -> None:
    """Covers: CHKCLI-002"""
    registry.register(_Pass())
    result = runner.invoke(check_app, ["--path", "."])
    assert result.exit_code == 0
    assert "a-ok" in result.stdout


def test_check_help() -> None:
    """Covers: CHKCLI-003"""
    result = runner.invoke(check_app, ["--help"])
    assert result.exit_code == 0
    # Verify that the command accepts --path by testing it
    registry.register(_Pass())
    result = runner.invoke(check_app, ["--path", "."])
    assert result.exit_code == 0
    assert "a-ok" in result.stdout


# ---------------------------------------------------------------------------
# 4.3 / 4.4 — Output formatting
# ---------------------------------------------------------------------------


def test_output_all_pass() -> None:
    """Covers: CHKCLI-004"""
    registry.register(_Pass())
    result = runner.invoke(check_app)
    assert result.exit_code == 0
    assert "[PASS]" in result.stdout
    assert "1 check(s): 1 passed" in result.stdout
    assert "failed" not in result.stdout.lower()
    assert "warning" not in result.stdout.lower()


def test_output_one_fail() -> None:
    """Covers: CHKCLI-005"""
    registry.register(_Fail())
    result = runner.invoke(check_app)
    assert result.exit_code == 2
    assert "[FAIL]" in result.stdout
    assert "something wrong" in result.stdout
    assert "1 failed" in result.stdout


def test_output_mixed() -> None:
    """Covers: CHKCLI-006"""
    registry.register(_Pass())
    registry.register(_Warn())
    registry.register(_Fail())
    result = runner.invoke(check_app)
    assert result.exit_code == 2
    assert "[PASS]" in result.stdout
    assert "[WARN]" in result.stdout
    assert "[FAIL]" in result.stdout
    assert "1 passed" in result.stdout
    assert "1 warning(s)" in result.stdout
    assert "1 failed" in result.stdout


def test_output_registration_order() -> None:
    """Covers: CHKCLI-010"""
    registry.register(_Fail())  # registered first
    registry.register(_Pass())  # registered second
    result = runner.invoke(check_app)
    assert result.exit_code == 2
    assert result.stdout.index("[FAIL]") < result.stdout.index("[PASS]")


# ---------------------------------------------------------------------------
# 4.5 / 4.6 — Exit codes
# ---------------------------------------------------------------------------


def test_exit_code_zero_all_pass() -> None:
    """Covers: CHKCLI-007"""
    registry.register(_Pass())
    result = runner.invoke(check_app)
    assert result.exit_code == 0


def test_exit_code_one_warnings_only() -> None:
    """Covers: CHKCLI-008"""
    registry.register(_Warn())
    result = runner.invoke(check_app)
    assert result.exit_code == 1


def test_exit_code_two_failures() -> None:
    """Covers: CHKCLI-009"""
    registry.register(_Fail())
    result = runner.invoke(check_app)
    assert result.exit_code == 2


def test_exit_code_two_failures_and_warnings() -> None:
    """Covers: CHKCLI-009 — failures take precedence over warnings"""
    registry.register(_Warn())
    registry.register(_Fail())
    result = runner.invoke(check_app)
    assert result.exit_code == 2


# ---------------------------------------------------------------------------
# 4.8 — iec --help smoke test
# ---------------------------------------------------------------------------


def test_ase_help_lists_check() -> None:
    """`iec --help` lists the `check` command."""
    from iec_cli.main import app

    result = runner.invoke(app, ["--help"])
    assert "check" in result.stdout
