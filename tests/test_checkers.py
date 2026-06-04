"""Unit tests for agent-facing file checkers."""

from pathlib import Path

import pytest

from iec_cli.check import Registry, Status
from iec_cli.checkers import agents_exists, agents_links, agents_size

# ---------------------------------------------------------------------------
# agents-exists
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.ac("AGEX-001")
def test_agents_exists_found(tmp_path: Path) -> None:
    """Covers: AGEX-001"""
    (tmp_path / "AGENTS.md").write_text("# Project")
    result = agents_exists.AgentsExists().check(tmp_path)
    assert result.status == Status.PASS
    assert "found" in result.message


@pytest.mark.unit
@pytest.mark.ac("AGEX-002")
def test_agents_exists_missing(tmp_path: Path) -> None:
    """Covers: AGEX-002"""
    result = agents_exists.AgentsExists().check(tmp_path)
    assert result.status == Status.FAIL
    assert "not found" in result.message.lower()


@pytest.mark.unit
@pytest.mark.ac("AGEX-003")
def test_agents_exists_registered() -> None:
    """Covers: AGEX-003"""
    reg = Registry()
    reg.register(agents_exists.AgentsExists())
    assert "agents-exists" in [c[0] for c in reg.list_all()]


# ---------------------------------------------------------------------------
# agents-size
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.ac("AGSZ-001")
def test_agents_size_under_limit(tmp_path: Path) -> None:
    """Covers: AGSZ-001"""
    (tmp_path / "AGENTS.md").write_text("\n".join(f"line {i}" for i in range(30)))
    result = agents_size.AgentsSize().check(tmp_path)
    assert result.status == Status.PASS
    assert "30 lines" in result.message


@pytest.mark.unit
@pytest.mark.ac("AGSZ-002")
def test_agents_size_exceeds_limit(tmp_path: Path) -> None:
    """Covers: AGSZ-002"""
    (tmp_path / "AGENTS.md").write_text("\n".join(f"line {i}" for i in range(72)))
    result = agents_size.AgentsSize().check(tmp_path)
    assert result.status == Status.FAIL
    assert "72 lines" in result.message


@pytest.mark.unit
@pytest.mark.ac("AGSZ-003")
def test_agents_size_env_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Covers: AGSZ-003"""
    monkeypatch.setenv("ASE_AGENTS_MAX_LINES", "100")
    (tmp_path / "AGENTS.md").write_text("\n".join(f"line {i}" for i in range(80)))
    result = agents_size.AgentsSize().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("AGSZ-004")
def test_agents_size_missing_file(tmp_path: Path) -> None:
    """Covers: AGSZ-004"""
    result = agents_size.AgentsSize().check(tmp_path)
    assert result.status == Status.FAIL
    assert "not found" in result.message.lower()


@pytest.mark.unit
@pytest.mark.ac("AGSZ-005")
def test_agents_size_invalid_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Covers: AGSZ-005"""
    monkeypatch.setenv("ASE_AGENTS_MAX_LINES", "not-a-number")
    (tmp_path / "AGENTS.md").write_text("\n".join(f"line {i}" for i in range(30)))
    result = agents_size.AgentsSize().check(tmp_path)
    assert result.status == Status.PASS  # falls back to default 50


@pytest.mark.unit
@pytest.mark.ac("AGSZ-006")
def test_agents_size_registered() -> None:
    """Covers: AGSZ-006"""
    reg = Registry()
    reg.register(agents_size.AgentsSize())
    assert "agents-size" in [c[0] for c in reg.list_all()]


# ---------------------------------------------------------------------------
# agents-links
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.ac("AGLN-001")
def test_agents_links_all_described(tmp_path: Path) -> None:
    """Covers: AGLN-001"""
    (tmp_path / "AGENTS.md").write_text(
        "- [Build](build.md) -- ci instructions\n- [Test](test.md) -- test docs\n"
    )
    result = agents_links.AgentsLinks().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("AGLN-002")
def test_agents_links_bare_link(tmp_path: Path) -> None:
    """Covers: AGLN-002"""
    (tmp_path / "AGENTS.md").write_text("- [Build](build.md)\n")
    result = agents_links.AgentsLinks().check(tmp_path)
    assert result.status == Status.WARN
    assert "build.md" in result.message


@pytest.mark.unit
@pytest.mark.ac("AGLN-003")
def test_agents_links_multiple_bare(tmp_path: Path) -> None:
    """Covers: AGLN-003"""
    (tmp_path / "AGENTS.md").write_text("- [Build](build.md)\n- [Test](test.md)\n")
    result = agents_links.AgentsLinks().check(tmp_path)
    assert result.status == Status.WARN
    assert "build.md" in result.message
    assert "test.md" in result.message


@pytest.mark.unit
@pytest.mark.ac("AGLN-005")
def test_agents_links_missing_file(tmp_path: Path) -> None:
    """Covers: AGLN-005"""
    result = agents_links.AgentsLinks().check(tmp_path)
    assert result.status == Status.FAIL
    assert "not found" in result.message.lower()


@pytest.mark.unit
@pytest.mark.ac("AGLN-004")
def test_agents_links_non_list_bare_link(tmp_path: Path) -> None:
    """Covers: AGLN-004 — bare link in paragraph line is still flagged."""
    (tmp_path / "AGENTS.md").write_text("Read [Build](build.md)\n")
    result = agents_links.AgentsLinks().check(tmp_path)
    assert result.status == Status.WARN
    assert "build.md" in result.message


@pytest.mark.unit
@pytest.mark.ac("AGLN-006")
def test_agents_links_registered() -> None:
    """Covers: AGLN-006"""
    reg = Registry()
    reg.register(agents_links.AgentsLinks())
    assert "agents-links" in [c[0] for c in reg.list_all()]
