"""Unit tests for hub structure and secrets checkers."""

from pathlib import Path

import pytest

from iec_cli.check import Registry, Status
from iec_cli.checkers import agents_hub_structure, secrets

# Fake credential strings constructed at runtime so the source file itself
# does not trigger the secrets scanner when iec check runs on this repo.
_FAKE_AWS_KEY = "AKIA" + "IOSFODNN7EXAMPLE"
_FAKE_PEM_LINE = "-----" + "BEGIN RSA PRIVATE KEY" + "-----"
_FAKE_CRED_LINE = "api_" + 'key = "sk-abc1234567890xyz"'


# ---------------------------------------------------------------------------
# agents-hub-structure
# ---------------------------------------------------------------------------


def _make_hub(
    base: Path, with_instructions: bool = True, with_skills: bool = True
) -> None:
    agents_dir = base / ".agents"
    agents_dir.mkdir()
    if with_instructions:
        (agents_dir / "instructions").mkdir()
    if with_skills:
        (agents_dir / "skills").mkdir()


@pytest.mark.unit
@pytest.mark.ac("AHUB-001")
def test_hub_structure_complete(tmp_path: Path) -> None:
    """Covers: AHUB-001"""
    _make_hub(tmp_path)
    result = agents_hub_structure.AgentsHubStructure().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("AHUB-002")
def test_hub_structure_missing_agents_dir(tmp_path: Path) -> None:
    """Covers: AHUB-002"""
    result = agents_hub_structure.AgentsHubStructure().check(tmp_path)
    assert result.status == Status.FAIL
    assert ".agents/" in result.message


@pytest.mark.unit
@pytest.mark.ac("AHUB-003")
def test_hub_structure_missing_instructions(tmp_path: Path) -> None:
    """Covers: AHUB-003"""
    _make_hub(tmp_path, with_instructions=False)
    result = agents_hub_structure.AgentsHubStructure().check(tmp_path)
    assert result.status == Status.FAIL
    assert "instructions/" in result.message


@pytest.mark.unit
@pytest.mark.ac("AHUB-004")
def test_hub_structure_missing_skills(tmp_path: Path) -> None:
    """Covers: AHUB-004"""
    _make_hub(tmp_path, with_skills=False)
    result = agents_hub_structure.AgentsHubStructure().check(tmp_path)
    assert result.status == Status.FAIL
    assert "skills/" in result.message


@pytest.mark.unit
@pytest.mark.ac("AHUB-005")
def test_hub_structure_missing_both(tmp_path: Path) -> None:
    """Covers: AHUB-005"""
    (tmp_path / ".agents").mkdir()
    result = agents_hub_structure.AgentsHubStructure().check(tmp_path)
    assert result.status == Status.FAIL
    assert "instructions/" in result.message
    assert "skills/" in result.message


@pytest.mark.unit
@pytest.mark.ac("AHUB-006")
def test_hub_structure_registered() -> None:
    """Covers: AHUB-006"""
    reg = Registry()
    reg.register(agents_hub_structure.AgentsHubStructure)
    assert "agents-hub-structure" in [c[0] for c in reg.list_all()]


# ---------------------------------------------------------------------------
# secrets
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.ac("SECR-001")
def test_secrets_clean(tmp_path: Path) -> None:
    """Covers: SECR-001"""
    (tmp_path / "README.md").write_text("# Hello World\n\nNo secrets here.\n")
    result = secrets.Secrets().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("SECR-002")
def test_secrets_aws_key(tmp_path: Path) -> None:
    """Covers: SECR-002"""
    (tmp_path / "config.py").write_text(f'AWS_KEY = "{_FAKE_AWS_KEY}"\n')
    result = secrets.Secrets().check(tmp_path)
    assert result.status == Status.FAIL
    assert "config.py" in result.message


@pytest.mark.unit
@pytest.mark.ac("SECR-003")
def test_secrets_private_key(tmp_path: Path) -> None:
    """Covers: SECR-003"""
    (tmp_path / "key.pem").write_text(f"{_FAKE_PEM_LINE}\nMIIEpAIB...\n")
    result = secrets.Secrets().check(tmp_path)
    assert result.status == Status.FAIL
    assert "key.pem" in result.message


@pytest.mark.unit
@pytest.mark.ac("SECR-004")
def test_secrets_credential_assignment(tmp_path: Path) -> None:
    """Covers: SECR-004"""
    (tmp_path / "settings.py").write_text(_FAKE_CRED_LINE + "\n")
    result = secrets.Secrets().check(tmp_path)
    assert result.status == Status.FAIL
    assert "settings.py" in result.message


@pytest.mark.unit
@pytest.mark.ac("SECR-005")
def test_secrets_skips_git_dir(tmp_path: Path) -> None:
    """Covers: SECR-005"""
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "secret.py").write_text(f'key = "{_FAKE_AWS_KEY}"\n')
    result = secrets.Secrets().check(tmp_path)
    assert result.status == Status.PASS


@pytest.mark.unit
@pytest.mark.ac("SECR-006")
def test_secrets_registered() -> None:
    """Covers: SECR-006"""
    reg = Registry()
    reg.register(secrets.Secrets)
    assert "secrets" in [c[0] for c in reg.list_all()]
