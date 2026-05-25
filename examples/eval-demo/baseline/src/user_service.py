class UserService:
    def create_user(self, name: str, email: str) -> dict:
        self._validate_email(email)
        return {"name": name, "email": email}

    def _validate_email(self, email: str) -> None:
        if "@" not in email:
            raise ValueError(f"Invalid email: {email}")
