"""Smoke tests for the iec-cli package."""

import pytest

import iec_cli


@pytest.mark.sanity
def test_package_importable() -> None:
    """Verify the package can be imported."""
    assert iec_cli is not None


@pytest.mark.sanity
def test_cli_app_exists() -> None:
    """Verify the Typer app entry point exists."""
    from iec_cli.main import app

    assert app is not None
    # Typer app has a registered callback
    assert app.registered_callback is not None
