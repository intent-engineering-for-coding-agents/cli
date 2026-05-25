import pytest

from src.user_service import UserService


@pytest.mark.ac("USER-001")
def test_create_user_valid() -> None:
    svc = UserService()
    result = svc.create_user("Alice", "alice@example.com")
    assert result["name"] == "Alice"
    assert result["email"] == "alice@example.com"


@pytest.mark.ac("USER-002")
def test_create_user_invalid_email() -> None:
    svc = UserService()
    with pytest.raises(ValueError):
        svc.create_user("Alice", "not-an-email")
