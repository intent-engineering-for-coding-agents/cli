def validate_email(email: str) -> None:
    if "@" not in email:
        raise ValueError(f"Invalid email: {email}")


def create_user(name: str, email: str) -> dict:
    validate_email(email)
    return {"name": name, "email": email}
