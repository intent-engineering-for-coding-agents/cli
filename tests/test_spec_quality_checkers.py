"""Unit tests for spec quality checkers (spec-ac-ids, spec-test-category)."""

from pathlib import Path

from ase_cli.check import Registry, Status
from ase_cli.checkers import spec_ac_ids, spec_test_category


def _write_spec(base: Path, name: str, content: str) -> Path:
    spec_file = base / "openspec" / "specs" / name / "spec.md"
    spec_file.parent.mkdir(parents=True, exist_ok=True)
    spec_file.write_text(content)
    return spec_file


# ---------------------------------------------------------------------------
# spec-ac-ids
# ---------------------------------------------------------------------------

_SPEC_ALL_AC_IDS = """\
## Requirement: Foo

#### Scenario: Happy path [ACID-001]

Test-type: unit

- **WHEN** something
- **THEN** result
"""

_SPEC_MISSING_AC_ID = """\
## Requirement: Foo

#### Scenario: Happy path

Test-type: unit

- **WHEN** something
- **THEN** result
"""

_SPEC_MIXED_AC_IDS = """\
#### Scenario: Has AC ID [ACID-001]

Test-type: unit

#### Scenario: Missing AC ID

Test-type: unit
"""


def test_spec_ac_ids_no_spec_files(tmp_path: Path) -> None:
    """Covers: ACID-001"""
    result = spec_ac_ids.SpecAcIds().check(tmp_path)
    assert result.status == Status.PASS


def test_spec_ac_ids_all_present(tmp_path: Path) -> None:
    """Covers: ACID-002"""
    _write_spec(tmp_path, "my-spec", _SPEC_ALL_AC_IDS)
    result = spec_ac_ids.SpecAcIds().check(tmp_path)
    assert result.status == Status.PASS


def test_spec_ac_ids_missing(tmp_path: Path) -> None:
    """Covers: ACID-003"""
    _write_spec(tmp_path, "my-spec", _SPEC_MISSING_AC_ID)
    result = spec_ac_ids.SpecAcIds().check(tmp_path)
    assert result.status == Status.FAIL
    assert "Happy path" in result.message


def test_spec_ac_ids_multiple_one_missing(tmp_path: Path) -> None:
    """Covers: ACID-004"""
    _write_spec(tmp_path, "my-spec", _SPEC_MIXED_AC_IDS)
    result = spec_ac_ids.SpecAcIds().check(tmp_path)
    assert result.status == Status.FAIL
    assert "Missing AC ID" in result.message


def test_spec_ac_ids_registered() -> None:
    """Covers: ACID-005"""
    reg = Registry()
    reg.register(spec_ac_ids.SpecAcIds)
    assert "spec-ac-ids" in [c[0] for c in reg.list_all()]


# ---------------------------------------------------------------------------
# spec-test-category
# ---------------------------------------------------------------------------

_SPEC_ALL_TEST_FIELDS = """\
#### Scenario: Happy path [STCT-001]

Test-type: unit

- **WHEN** something
- **THEN** result
"""

_SPEC_MISSING_TEST_FIELD = """\
#### Scenario: Happy path [STCT-001]

- **WHEN** something
- **THEN** result
"""

_SPEC_MIXED_TEST_FIELDS = """\
#### Scenario: Has Test field [STCT-001]

Test-type: unit

- **WHEN** something

#### Scenario: Missing Test field [STCT-002]

- **WHEN** something else
"""


def test_spec_test_category_no_spec_files(tmp_path: Path) -> None:
    """Covers: STCT-001"""
    result = spec_test_category.SpecTestCategory().check(tmp_path)
    assert result.status == Status.PASS


def test_spec_test_category_all_present(tmp_path: Path) -> None:
    """Covers: STCT-002"""
    _write_spec(tmp_path, "my-spec", _SPEC_ALL_TEST_FIELDS)
    result = spec_test_category.SpecTestCategory().check(tmp_path)
    assert result.status == Status.PASS


def test_spec_test_category_missing(tmp_path: Path) -> None:
    """Covers: STCT-003"""
    _write_spec(tmp_path, "my-spec", _SPEC_MISSING_TEST_FIELD)
    result = spec_test_category.SpecTestCategory().check(tmp_path)
    assert result.status == Status.FAIL
    assert "Happy path" in result.message


def test_spec_test_category_multiple_one_missing(tmp_path: Path) -> None:
    """Covers: STCT-004"""
    _write_spec(tmp_path, "my-spec", _SPEC_MIXED_TEST_FIELDS)
    result = spec_test_category.SpecTestCategory().check(tmp_path)
    assert result.status == Status.FAIL
    assert "Missing Test field" in result.message


def test_spec_test_category_registered() -> None:
    """Covers: STCT-005"""
    reg = Registry()
    reg.register(spec_test_category.SpecTestCategory)
    assert "spec-test-category" in [c[0] for c in reg.list_all()]
