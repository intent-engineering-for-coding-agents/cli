import pytest

from src.user_service import create_user, validate_email


def test_create_user_valid() -> None:
    result = create_user("Alice", "alice@example.com")
    assert result["name"] == "Alice"
    assert result["email"] == "alice@example.com"


def test_invalid_email() -> None:
    with pytest.raises(ValueError):
        validate_email("not-an-email")
