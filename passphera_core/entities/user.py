from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List, Optional

class User:
    def __init__(self, id: UUID = None, email: str = None, username: str = None):
        self.id = id or uuid4()
        self.email = email
        self.username = username
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        self.passwords: List["Password"] = []
        self.generator: Optional["Generator"] = None

    def update_email(self, new_email: str):
        if "@" not in new_email:
            raise ValueError("Invalid email address")
        self.email = new_email
        self.updated_at = datetime.now(timezone.utc)

    def add_password(self, password: "Password"):
        self.passwords.append(password)
        self.updated_at = datetime.now(timezone.utc)
