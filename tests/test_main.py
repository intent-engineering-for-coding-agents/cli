"""Smoke tests for the ase-cli package."""

import ase_cli


def test_package_importable() -> None:
    """Verify the package can be imported."""
    assert ase_cli is not None


def test_cli_app_exists() -> None:
    """Verify the Typer app entry point exists."""
    from ase_cli.main import app

    assert app is not None
    # Typer app has a registered callback
    assert app.registered_callback is not None
