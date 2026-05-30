"""Unit tests for test-traceability and test-coverage checkers."""

from pathlib import Path

from ase_cli.check import Registry, Status
from ase_cli.checkers import test_coverage, test_traceability


def _write_spec(base: Path, name: str, content: str) -> Path:
    spec_file = base / "openspec" / "specs" / name / "spec.md"
    spec_file.parent.mkdir(parents=True, exist_ok=True)
    spec_file.write_text(content)
    return spec_file


def _write_test(base: Path, name: str, content: str) -> Path:
    test_file = base / "tests" / name
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text(content)
    return test_file


# ---------------------------------------------------------------------------
# Spec fixtures
# ---------------------------------------------------------------------------

_SPEC_ONE_AC = """\
#### Scenario: Happy path [FOO-001]

Test-type: Unit

- **WHEN** something
- **THEN** result
"""

_SPEC_MANUAL_AC = """\
#### Scenario: Manual check [FOO-002]

Test-type: Manual

- **WHEN** something
- **THEN** result
"""

_SPEC_TWO_ACS = """\
#### Scenario: First [FOO-001]

Test-type: Unit

- **WHEN** first
- **THEN** result

#### Scenario: Second [FOO-002]

Test-type: Unit

- **WHEN** second
- **THEN** result
"""

_PYTEST_FOO_001 = '@pytest.mark.ac("FOO-001")\ndef test_it(): pass\n'

# ---------------------------------------------------------------------------
# test-traceability
# ---------------------------------------------------------------------------


def test_traceability_no_spec_files(tmp_path: Path) -> None:
    """Covers: TRTC-001"""
    result = test_traceability.TestTraceability().check(tmp_path)
    assert result.status == Status.PASS


def test_traceability_all_covered(tmp_path: Path) -> None:
    """Covers: TRTC-002"""
    _write_spec(tmp_path, "my-spec", _SPEC_ONE_AC)
    _write_test(tmp_path, "test_foo.py", _PYTEST_FOO_001)
    result = test_traceability.TestTraceability().check(tmp_path)
    assert result.status == Status.PASS


def test_traceability_missing_marker(tmp_path: Path) -> None:
    """Covers: TRTC-003"""
    _write_spec(tmp_path, "my-spec", _SPEC_ONE_AC)
    result = test_traceability.TestTraceability().check(tmp_path)
    assert result.status == Status.FAIL
    assert "FOO-001" in result.message


def test_traceability_multiple_missing(tmp_path: Path) -> None:
    """Covers: TRTC-004"""
    _write_spec(tmp_path, "my-spec", _SPEC_TWO_ACS)
    result = test_traceability.TestTraceability().check(tmp_path)
    assert result.status == Status.FAIL
    assert "FOO-001" in result.message
    assert "FOO-002" in result.message


def test_traceability_manual_exempt(tmp_path: Path) -> None:
    """Covers: TRTC-005"""
    _write_spec(tmp_path, "my-spec", _SPEC_MANUAL_AC)
    result = test_traceability.TestTraceability().check(tmp_path)
    assert result.status == Status.PASS


def test_traceability_pytest_marker(tmp_path: Path) -> None:
    """Covers: TRTC-006"""
    _write_spec(tmp_path, "my-spec", _SPEC_ONE_AC)
    _write_test(tmp_path, "test_foo.py", _PYTEST_FOO_001)
    result = test_traceability.TestTraceability().check(tmp_path)
    assert result.status == Status.PASS


def test_traceability_junit_tag(tmp_path: Path) -> None:
    """Covers: TRTC-007"""
    _write_spec(tmp_path, "my-spec", _SPEC_ONE_AC)
    _write_test(tmp_path, "FooTest.java", '@Tag("FOO-001")\nvoid test() {}\n')
    result = test_traceability.TestTraceability().check(tmp_path)
    assert result.status == Status.PASS


def test_traceability_cucumber_tag(tmp_path: Path) -> None:
    """Covers: TRTC-008"""
    _write_spec(tmp_path, "my-spec", _SPEC_ONE_AC)
    _write_test(tmp_path, "foo.feature", "@AC:FOO-001\nScenario: ...\n")
    result = test_traceability.TestTraceability().check(tmp_path)
    assert result.status == Status.PASS


def test_traceability_inline_comment(tmp_path: Path) -> None:
    """Covers: TRTC-009"""
    _write_spec(tmp_path, "my-spec", _SPEC_ONE_AC)
    _write_test(tmp_path, "test_foo.py", "// AC: FOO-001\ndef test_it(): pass\n")
    result = test_traceability.TestTraceability().check(tmp_path)
    assert result.status == Status.PASS


def test_traceability_orphaned_marker(tmp_path: Path) -> None:
    """Covers: TRTC-010"""
    _write_spec(tmp_path, "my-spec", _SPEC_ONE_AC)
    _write_test(
        tmp_path,
        "test_foo.py",
        '@pytest.mark.ac("FOO-001")\ndef test_it(): pass\n'
        '@pytest.mark.ac("BAR-999")\ndef test_orphan(): pass\n',
    )
    result = test_traceability.TestTraceability().check(tmp_path)
    assert result.status == Status.WARN
    assert "BAR-999" in result.message


def test_traceability_registered() -> None:
    """Covers: TRTC-011"""
    reg = Registry()
    reg.register(test_traceability.TestTraceability)
    assert "test-traceability" in [c[0] for c in reg.list_all()]


# ---------------------------------------------------------------------------
# test-coverage
# ---------------------------------------------------------------------------


def test_coverage_no_spec_files(tmp_path: Path) -> None:
    """Covers: TCOV-001"""
    result = test_coverage.TestCoverage().check(tmp_path)
    assert result.status == Status.PASS


def test_coverage_all_have_two_markers(tmp_path: Path) -> None:
    """Covers: TCOV-002"""
    _write_spec(tmp_path, "my-spec", _SPEC_ONE_AC)
    _write_test(
        tmp_path,
        "test_foo.py",
        '@pytest.mark.ac("FOO-001")\ndef test_positive(): pass\n'
        '@pytest.mark.ac("FOO-001")\ndef test_negative(): pass\n',
    )
    result = test_coverage.TestCoverage().check(tmp_path)
    assert result.status == Status.PASS


def test_coverage_single_marker_warns(tmp_path: Path) -> None:
    """Covers: TCOV-003"""
    _write_spec(tmp_path, "my-spec", _SPEC_ONE_AC)
    _write_test(tmp_path, "test_foo.py", _PYTEST_FOO_001)
    result = test_coverage.TestCoverage().check(tmp_path)
    assert result.status == Status.WARN
    assert "FOO-001" in result.message


def test_coverage_multiple_under_covered(tmp_path: Path) -> None:
    """Covers: TCOV-004"""
    _write_spec(tmp_path, "my-spec", _SPEC_TWO_ACS)
    _write_test(
        tmp_path,
        "test_foo.py",
        '@pytest.mark.ac("FOO-001")\ndef test_a(): pass\n'
        '@pytest.mark.ac("FOO-002")\ndef test_b(): pass\n',
    )
    result = test_coverage.TestCoverage().check(tmp_path)
    assert result.status == Status.WARN
    assert "FOO-001" in result.message
    assert "FOO-002" in result.message


def test_coverage_manual_exempt(tmp_path: Path) -> None:
    """Covers: TCOV-005"""
    _write_spec(tmp_path, "my-spec", _SPEC_MANUAL_AC)
    result = test_coverage.TestCoverage().check(tmp_path)
    assert result.status == Status.PASS


def test_coverage_zero_markers_not_reported(tmp_path: Path) -> None:
    """Covers: TCOV-006 — uncovered ACs belong to test-traceability."""
    _write_spec(tmp_path, "my-spec", _SPEC_ONE_AC)
    result = test_coverage.TestCoverage().check(tmp_path)
    assert result.status == Status.PASS


def test_coverage_registered() -> None:
    """Covers: TCOV-007"""
    reg = Registry()
    reg.register(test_coverage.TestCoverage)
    assert "test-coverage" in [c[0] for c in reg.list_all()]
