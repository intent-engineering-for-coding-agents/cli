"""Unit tests for size checkers (spec-size, file-size)."""

from pathlib import Path

import pytest

from ase_cli.check import Registry, Status
from ase_cli.checkers import file_size, spec_size


def _write_spec(base: Path, content: str) -> Path:
    spec_file = base / "openspec" / "specs" / "my-spec" / "spec.md"
    spec_file.parent.mkdir(parents=True, exist_ok=True)
    spec_file.write_text(content)
    return spec_file


# ---------------------------------------------------------------------------
# spec-size
# ---------------------------------------------------------------------------


def test_spec_size_no_spec_files(tmp_path: Path) -> None:
    """Covers: SPSZ-004"""
    result = spec_size.SpecSize().check(tmp_path)
    assert result.status == Status.PASS


def test_spec_size_under_limit(tmp_path: Path) -> None:
    """Covers: SPSZ-001"""
    _write_spec(tmp_path, "\n".join(f"line {i}" for i in range(100)))
    result = spec_size.SpecSize().check(tmp_path)
    assert result.status == Status.PASS


def test_spec_size_over_limit(tmp_path: Path) -> None:
    """Covers: SPSZ-002"""
    _write_spec(tmp_path, "\n".join(f"line {i}" for i in range(600)))
    result = spec_size.SpecSize().check(tmp_path)
    assert result.status == Status.WARN
    assert "600 lines" in result.message


def test_spec_size_env_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Covers: SPSZ-003"""
    monkeypatch.setenv("ASE_SPEC_MAX_LINES", "50")
    _write_spec(tmp_path, "\n".join(f"line {i}" for i in range(80)))
    result = spec_size.SpecSize().check(tmp_path)
    assert result.status == Status.WARN


def test_spec_size_invalid_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Covers: SPSZ-005"""
    monkeypatch.setenv("ASE_SPEC_MAX_LINES", "not-a-number")
    _write_spec(tmp_path, "\n".join(f"line {i}" for i in range(100)))
    result = spec_size.SpecSize().check(tmp_path)
    assert result.status == Status.PASS  # falls back to default 500


def test_spec_size_registered() -> None:
    """Covers: SPSZ-006"""
    reg = Registry()
    reg.register(spec_size.SpecSize)
    assert "spec-size" in [c[0] for c in reg.list_all()]


# ---------------------------------------------------------------------------
# file-size
# ---------------------------------------------------------------------------


def test_file_size_no_md_files(tmp_path: Path) -> None:
    """Covers: FLSZ-004"""
    result = file_size.FileSize().check(tmp_path)
    assert result.status == Status.PASS


def test_file_size_under_limit(tmp_path: Path) -> None:
    """Covers: FLSZ-001"""
    (tmp_path / "README.md").write_text("\n".join(f"line {i}" for i in range(100)))
    result = file_size.FileSize().check(tmp_path)
    assert result.status == Status.PASS


def test_file_size_over_limit(tmp_path: Path) -> None:
    """Covers: FLSZ-002"""
    (tmp_path / "README.md").write_text("\n".join(f"line {i}" for i in range(600)))
    result = file_size.FileSize().check(tmp_path)
    assert result.status == Status.WARN
    assert "600 lines" in result.message


def test_file_size_env_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Covers: FLSZ-003"""
    monkeypatch.setenv("ASE_FILE_MAX_LINES", "50")
    (tmp_path / "README.md").write_text("\n".join(f"line {i}" for i in range(80)))
    result = file_size.FileSize().check(tmp_path)
    assert result.status == Status.WARN


def test_file_size_skips_node_modules(tmp_path: Path) -> None:
    """Covers: FLSZ-005"""
    pkg_dir = tmp_path / "node_modules" / "some-pkg"
    pkg_dir.mkdir(parents=True)
    (pkg_dir / "README.md").write_text("\n".join(f"line {i}" for i in range(600)))
    result = file_size.FileSize().check(tmp_path)
    assert result.status == Status.PASS


def test_file_size_invalid_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Covers: FLSZ-006"""
    monkeypatch.setenv("ASE_FILE_MAX_LINES", "not-a-number")
    (tmp_path / "README.md").write_text("\n".join(f"line {i}" for i in range(100)))
    result = file_size.FileSize().check(tmp_path)
    assert result.status == Status.PASS  # falls back to default 500


def test_file_size_registered() -> None:
    """Covers: FLSZ-007"""
    reg = Registry()
    reg.register(file_size.FileSize)
    assert "file-size" in [c[0] for c in reg.list_all()]
