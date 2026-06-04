"""Integration tests for iec init command."""

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from iec_cli.main import app

runner = CliRunner()


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-001")
def test_init_in_empty_directory(tmp_path: Path) -> None:
    """SCAFFOLD-001: Init creates all directories and stub files in empty target."""
    result = runner.invoke(app, ["init", "--path", str(tmp_path)])

    assert result.exit_code == 0

    expected_dirs = [
        "docs/architecture",
        "docs/decisions",
        "docs/design",
        "openspec/changes/archive",
        "openspec/specs",
        ".agents/instructions",
        ".agents/commands",
        ".agents/skills",
        ".agents/hooks",
    ]
    for d in expected_dirs:
        assert (tmp_path / d).is_dir(), f"Missing directory: {d}"

    expected_files = [
        "AGENTS.md",
        "docs/README.md",
        "docs/INDEX.md",
        "docs/testing-convention.md",
        "docs/testing-strategy.md",
        "docs/decisions/README.md",
        "docs/design/README.md",
    ]
    for f in expected_files:
        assert (tmp_path / f).is_file(), f"Missing file: {f}"

    assert "Created directory:" in result.stdout
    assert "Created file:" in result.stdout


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-014")
def test_init_gitkeep_in_empty_dirs(tmp_path: Path) -> None:
    """SCAFFOLD-014: .gitkeep files placed in directories that stay empty."""
    result = runner.invoke(app, ["init", "--path", str(tmp_path)])
    assert result.exit_code == 0

    gitkeep_dirs = [
        "docs/architecture",
        "openspec/changes/archive",
        "openspec/specs",
        ".agents/instructions",
        ".agents/commands",
        ".agents/skills",
        ".agents/hooks",
    ]
    for d in gitkeep_dirs:
        assert (tmp_path / d / ".gitkeep").is_file(), f"Missing .gitkeep in {d}"

    # Directories with stub files should NOT have .gitkeep
    assert not (tmp_path / "docs/decisions/.gitkeep").exists()
    assert not (tmp_path / "docs/design/.gitkeep").exists()


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-015")
def test_help_shows_commands() -> None:
    """SCAFFOLD-015: --help shows available commands."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "init" in result.stdout
    assert "Scaffold" in result.stdout


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-016")
def test_version_shows_number() -> None:
    """SCAFFOLD-016: --version shows version from pyproject.toml."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0." in result.stdout


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-002")
def test_init_partial_structure(tmp_path: Path) -> None:
    """SCAFFOLD-002: Partial init — missing created, existing preserved."""
    # Pre-create one directory and one file
    (tmp_path / "docs" / "architecture").mkdir(parents=True)
    (tmp_path / "AGENTS.md").write_text("existing content")

    result = runner.invoke(app, ["init", "--path", str(tmp_path)])

    assert result.exit_code == 0
    # Existing file preserved
    assert (tmp_path / "AGENTS.md").read_text() == "existing content"
    # Missing items created
    assert (tmp_path / "docs/decisions").is_dir()
    assert (tmp_path / "docs/README.md").is_file()


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-003")
def test_init_fully_initialized(tmp_path: Path) -> None:
    """SCAFFOLD-003: Init in fully initialized directory reports nothing to do."""
    # Run init once
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    # Run again
    result = runner.invoke(app, ["init", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Already initialized" in result.stdout


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-004")
def test_agents_md_content(tmp_path: Path) -> None:
    """SCAFFOLD-004: AGENTS.md follows TOC pattern with project name, under 25 lines."""
    result = runner.invoke(app, ["init", "--path", str(tmp_path)])
    assert result.exit_code == 0

    content = (tmp_path / "AGENTS.md").read_text()

    assert "# AGENTS.md" in content
    assert "docs/INDEX.md" in content
    assert "**Language**" in content
    assert "**Framework**" in content
    assert len(content.splitlines()) <= 25


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-005")
@pytest.mark.ac("SCAFFOLD-006")
def test_init_dry_run(tmp_path: Path) -> None:
    """SCAFFOLD-005/006: --dry-run lists files, no filesystem changes."""
    before = list(tmp_path.rglob("*"))

    result = runner.invoke(app, ["init", "--path", str(tmp_path), "--dry-run"])

    assert result.exit_code == 0
    assert "Would create" in result.stdout

    after = list(tmp_path.rglob("*"))
    assert len(after) == len(before)


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-007")
@pytest.mark.ac("SCAFFOLD-008")
def test_init_force_overwrites(tmp_path: Path) -> None:
    """SCAFFOLD-007/008: --force overwrites existing files."""
    # Create existing AGENTS.md with custom content
    (tmp_path / "AGENTS.md").write_text("custom content")
    # Also pre-create full dir structure
    runner.invoke(app, ["init", "--path", str(tmp_path)])

    # Force re-init
    result = runner.invoke(app, ["init", "--path", str(tmp_path), "--force"])

    assert result.exit_code == 0
    content = (tmp_path / "AGENTS.md").read_text()
    assert "custom content" not in content
    assert "# AGENTS.md" in content


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-009")
@pytest.mark.ac("SCAFFOLD-010")
@pytest.mark.ac("SCAFFOLD-011")
def test_init_with_path(tmp_path: Path) -> None:
    """SCAFFOLD-009/010/011: --path targets a specific directory."""
    target = tmp_path / "subdir"

    result = runner.invoke(app, ["init", "--path", str(target)])

    assert result.exit_code == 0
    assert (target / "AGENTS.md").is_file()
    assert (target / "docs").is_dir()
    # Target dir created if missing
    assert target.is_dir()


@pytest.mark.integration
@pytest.mark.ac("VENDOR-001")
@pytest.mark.ac("VENDOR-004")
def test_init_with_claude(tmp_path: Path) -> None:
    """VENDOR-001/004: --with-claude creates CLAUDE.md."""
    result = runner.invoke(app, ["init", "--path", str(tmp_path), "--with-claude"])

    assert result.exit_code == 0
    assert (tmp_path / "CLAUDE.md").is_file()
    assert (tmp_path / "CLAUDE.md").read_text().strip() == "@AGENTS.md"


@pytest.mark.integration
@pytest.mark.ac("VENDOR-002")
def test_init_with_claude_existing_preserved(tmp_path: Path) -> None:
    """VENDOR-002: existing CLAUDE.md not overwritten without --force."""
    (tmp_path / "CLAUDE.md").write_text("custom claude content")

    result = runner.invoke(app, ["init", "--path", str(tmp_path), "--with-claude"])

    assert result.exit_code == 0
    assert (tmp_path / "CLAUDE.md").read_text() == "custom claude content"


@pytest.mark.integration
@pytest.mark.ac("VENDOR-003")
def test_init_with_claude_force(tmp_path: Path) -> None:
    """VENDOR-003: --with-claude --force overwrites existing CLAUDE.md."""
    (tmp_path / "CLAUDE.md").write_text("custom claude content")

    result = runner.invoke(
        app, ["init", "--path", str(tmp_path), "--with-claude", "--force"]
    )

    assert result.exit_code == 0
    assert (tmp_path / "CLAUDE.md").read_text().strip() == "@AGENTS.md"


@pytest.mark.integration
@pytest.mark.ac("VENDOR-005")
def test_init_with_gemini(tmp_path: Path) -> None:
    """VENDOR-005: --with-gemini creates .gemini/settings.json."""
    result = runner.invoke(app, ["init", "--path", str(tmp_path), "--with-gemini"])

    assert result.exit_code == 0
    settings = tmp_path / ".gemini" / "settings.json"
    assert settings.is_file()
    data = json.loads(settings.read_text())
    assert data["context"]["fileName"] == "AGENTS.md"


@pytest.mark.integration
@pytest.mark.ac("VENDOR-006")
def test_init_with_gemini_existing_preserved(tmp_path: Path) -> None:
    """VENDOR-006: existing .gemini/settings.json not overwritten without --force."""
    (tmp_path / ".gemini").mkdir(parents=True)
    (tmp_path / ".gemini" / "settings.json").write_text('{"old": true}')

    result = runner.invoke(app, ["init", "--path", str(tmp_path), "--with-gemini"])

    assert result.exit_code == 0
    assert (tmp_path / ".gemini" / "settings.json").read_text() == '{"old": true}'


@pytest.mark.integration
@pytest.mark.ac("VENDOR-007")
def test_init_both_vendor_flags(tmp_path: Path) -> None:
    """VENDOR-007: --with-claude --with-gemini creates both vendor files."""
    result = runner.invoke(
        app,
        ["init", "--path", str(tmp_path), "--with-claude", "--with-gemini"],
    )

    assert result.exit_code == 0
    assert (tmp_path / "CLAUDE.md").is_file()
    assert (tmp_path / ".gemini" / "settings.json").is_file()
    # Directory scaffolding also performed
    assert (tmp_path / "AGENTS.md").is_file()


@pytest.mark.integration
@pytest.mark.ac("VENDOR-008")
def test_vendor_dry_run(tmp_path: Path) -> None:
    """VENDOR-008: vendor --dry-run lists files but doesn't create."""
    result = runner.invoke(
        app,
        ["init", "--path", str(tmp_path), "--with-claude", "--dry-run"],
    )

    assert result.exit_code == 0
    assert "Would create" in result.stdout
    assert "CLAUDE.md" in result.stdout
    assert not (tmp_path / "CLAUDE.md").exists()


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-012")
def test_testing_convention_content(tmp_path: Path) -> None:
    """SCAFFOLD-012: testing-convention.md contains canonical content."""
    result = runner.invoke(app, ["init", "--path", str(tmp_path)])
    assert result.exit_code == 0

    content = (tmp_path / "docs" / "testing-convention.md").read_text()

    assert "Test Layers" in content
    assert "Unit" in content
    assert "Slice" in content
    assert "Integration" in content
    assert "E2E" in content
    assert "Performance" in content
    assert "Baseline" in content
    assert "AC ID" in content
    assert "[PREFIX-NNN]" in content
    assert "Test-type:" in content
    assert "Traceability Markers" in content
    assert len(content.splitlines()) <= 300


@pytest.mark.integration
@pytest.mark.ac("SCAFFOLD-013")
def test_testing_strategy_stub(tmp_path: Path) -> None:
    """SCAFFOLD-013: testing-strategy.md stub references convention."""
    result = runner.invoke(app, ["init", "--path", str(tmp_path)])
    assert result.exit_code == 0

    content = (tmp_path / "docs" / "testing-strategy.md").read_text()

    assert "testing-convention.md" in content
    assert "Test Layers" in content
    assert "AC ID Format" in content
    assert "Traceability Markers" in content
    assert "Test Directory Layout" in content
    assert "CI Wiring" in content
