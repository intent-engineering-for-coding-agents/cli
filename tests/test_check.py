"""Unit tests for check framework: enums, result model, protocol, registry."""

from pathlib import Path

import pytest

from iec_cli.check import Checker, CheckResult, Registry, Severity, Status, registry

# ---------------------------------------------------------------------------
# 1.1 — Enums
# ---------------------------------------------------------------------------


def test_status_enum_has_all_values() -> None:
    """Covers: CHKRSL-001"""
    assert Status.PASS.value == "PASS"
    assert Status.WARN.value == "WARN"
    assert Status.FAIL.value == "FAIL"
    assert len(Status) == 3


def test_severity_enum_has_all_values() -> None:
    """Covers: CHKRSL-002"""
    assert Severity.HIGH.value == "HIGH"
    assert Severity.MEDIUM.value == "MEDIUM"
    assert Severity.LOW.value == "LOW"
    assert len(Severity) == 3


# ---------------------------------------------------------------------------
# 1.2 / 1.3 — CheckResult dataclass and helpers
# ---------------------------------------------------------------------------


def test_check_result_all_fields() -> None:
    """Covers: CHKRSL-003"""
    result = CheckResult(
        check_id="agents-exists",
        status=Status.PASS,
        message="AGENTS.md found",
        severity=Severity.HIGH,
        location="AGENTS.md",
        ac_id="CHKRSL-003",
    )
    assert result.check_id == "agents-exists"
    assert result.status == Status.PASS
    assert result.message == "AGENTS.md found"
    assert result.severity == Severity.HIGH
    assert result.location == "AGENTS.md"
    assert result.ac_id == "CHKRSL-003"


def test_check_result_minimal_fields() -> None:
    """Covers: CHKRSL-004"""
    result = CheckResult(
        check_id="adr-format",
        status=Status.FAIL,
        message="Not MADR",
        severity=Severity.HIGH,
    )
    assert result.location is None
    assert result.ac_id is None


def test_check_result_equality() -> None:
    """Covers: CHKRSL-005"""
    a = CheckResult("x", Status.PASS, "ok", Severity.HIGH)
    b = CheckResult("x", Status.PASS, "ok", Severity.HIGH)
    c = CheckResult("x", Status.FAIL, "bad", Severity.HIGH)
    assert a == b
    assert a != c


def test_check_result_is_warning() -> None:
    """Covers: CHKRSL-006"""
    result = CheckResult("x", Status.WARN, "msg", Severity.MEDIUM)
    assert result.is_warning is True
    assert result.is_failure is False


def test_check_result_is_failure() -> None:
    """Covers: CHKRSL-007"""
    result = CheckResult("x", Status.FAIL, "msg", Severity.HIGH)
    assert result.is_warning is False
    assert result.is_failure is True


# ---------------------------------------------------------------------------
# 2.1 / 2.2 — Checker protocol
# ---------------------------------------------------------------------------


class ConformingChecker:
    id = "test-check"
    description = "A test checker"

    def check(self, path: Path) -> CheckResult:
        return CheckResult(self.id, Status.PASS, "ok", Severity.HIGH)


class MissingIdChecker:
    description = "Missing id"

    def check(self, path: Path) -> CheckResult:
        return CheckResult("", Status.PASS, "ok", Severity.HIGH)


class MissingCheckChecker:
    id = "no-check"
    description = "Missing check method"


def test_protocol_conformance() -> None:
    """Covers: CHKREG-004"""
    # ConformingChecker satisfies the Checker protocol structurally
    checker: Checker = ConformingChecker()
    assert checker.id == "test-check"
    assert checker.description == "A test checker"
    result = checker.check(Path("."))
    assert result.status == Status.PASS


def test_protocol_non_conforming_missing_id() -> None:
    """Covers: CHKREG-004 — negative: class without id does not conform"""
    # Verify MissingIdChecker has no 'id' attribute usable as str
    instance = MissingIdChecker()
    assert not hasattr(instance, "id")


def test_protocol_non_conforming_missing_check() -> None:
    """Covers: CHKREG-004 — negative: class without check method does not conform"""
    instance = MissingCheckChecker()
    has_check = hasattr(instance, "check")
    callable_check = callable(getattr(instance, "check", None))
    assert not has_check or not callable_check


# ---------------------------------------------------------------------------
# 3.1 / 3.2 / 3.3 — Registry: register and list_all
# ---------------------------------------------------------------------------


def test_register_checker_positive() -> None:
    """Covers: CHKREG-001"""
    reg = Registry()
    reg.register(ConformingChecker())
    assert "test-check" in [c[0] for c in reg.list_all()]


def test_register_typeerror_missing_id() -> None:
    """Covers: CHKREG-003"""
    reg = Registry()
    with pytest.raises(TypeError, match="'id'"):
        reg.register(MissingIdChecker())


def test_register_typeerror_missing_check() -> None:
    """Covers: CHKREG-003"""
    reg = Registry()
    with pytest.raises(TypeError, match="'check'"):
        reg.register(MissingCheckChecker())


def test_register_idempotent() -> None:
    """Covers: CHKREG-002"""
    reg = Registry()
    reg.register(ConformingChecker())
    reg.register(ConformingChecker())
    ids = [c[0] for c in reg.list_all()]
    assert ids.count("test-check") == 1


def test_list_all_returns_registration_order() -> None:
    """Covers: CHKREG-011"""

    class A:
        id = "b"
        description = "second"

        def check(self, path: Path) -> CheckResult:
            return CheckResult("b", Status.PASS, "", Severity.HIGH)

    class B:
        id = "a"
        description = "first"

        def check(self, path: Path) -> CheckResult:
            return CheckResult("a", Status.PASS, "", Severity.HIGH)

    class C:
        id = "c"
        description = "third"

        def check(self, path: Path) -> CheckResult:
            return CheckResult("c", Status.PASS, "", Severity.HIGH)

    reg = Registry()
    reg.register(A())
    reg.register(B())
    reg.register(C())
    assert reg.list_all() == [("b", "second"), ("a", "first"), ("c", "third")]


# ---------------------------------------------------------------------------
# 3.4 / 3.5 — Registry: run_all
# ---------------------------------------------------------------------------


def test_run_all_all_pass() -> None:
    """Covers: CHKREG-005"""
    reg = Registry()
    reg.register(ConformingChecker())

    class AlwaysPass:
        id = "always-pass"
        description = "Always passes"

        def check(self, path: Path) -> CheckResult:
            return CheckResult(self.id, Status.PASS, "ok", Severity.HIGH)

    reg.register(AlwaysPass())
    results = reg.run_all(Path("."))
    assert len(results) == 2
    assert all(r.status == Status.PASS for r in results)


def test_run_all_one_fails_others_continue() -> None:
    """Covers: CHKREG-006"""
    reg = Registry()

    class Failing:
        id = "failing"
        description = "Always fails"

        def check(self, path: Path) -> CheckResult:
            return CheckResult(self.id, Status.FAIL, "bad", Severity.HIGH)

    reg.register(ConformingChecker())
    reg.register(Failing())
    reg.register(ConformingChecker())  # Duplicate id is idempotent — need different id

    class AnotherPass:
        id = "another-pass"
        description = "Another pass"

        def check(self, path: Path) -> CheckResult:
            return CheckResult(self.id, Status.PASS, "ok", Severity.HIGH)

    reg.register(AnotherPass())

    results = reg.run_all(Path("."))
    assert len(results) == 3
    statuses = [r.status for r in results]
    assert statuses == [Status.PASS, Status.FAIL, Status.PASS]


def test_run_all_exception_caught() -> None:
    """Covers: CHKREG-007"""
    reg = Registry()

    class Broken:
        id = "broken"
        description = "Raises exception"

        def check(self, path: Path) -> CheckResult:
            raise RuntimeError("boom")

    reg.register(Broken())
    results = reg.run_all(Path("."))
    assert len(results) == 1
    assert results[0].status == Status.FAIL
    assert "boom" in results[0].message
    assert results[0].check_id == "broken"


def test_run_all_empty_registry() -> None:
    """Covers: CHKREG-008"""
    reg = Registry()
    results = reg.run_all(Path("."))
    assert results == []


# ---------------------------------------------------------------------------
# 3.6 / 3.7 — Registry: run_one
# ---------------------------------------------------------------------------


def test_run_one_existing_checker() -> None:
    """Covers: CHKREG-009"""
    reg = Registry()
    reg.register(ConformingChecker())
    result = reg.run_one("test-check", Path("."))
    assert result.status == Status.PASS
    assert result.check_id == "test-check"


def test_run_one_unknown_raises_keyerror() -> None:
    """Covers: CHKREG-010"""
    reg = Registry()
    with pytest.raises(KeyError, match="nonexistent"):
        reg.run_one("nonexistent", Path("."))


# ---------------------------------------------------------------------------
# 3.8 — Module-level registry instance
# ---------------------------------------------------------------------------


def test_module_registry_is_registry_instance() -> None:
    """Module-level `registry` is a usable Registry instance."""
    assert isinstance(registry, Registry)
