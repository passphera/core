from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from cryptography.fernet import Fernet

from passphera_core.utils import security


@dataclass
class Password:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    context: str = field(default_factory=str)
    text: str = field(default_factory=str)
    password: str = field(default_factory=str)
    salt: bytes = field(default_factory=bytes)

    def encrypt(self) -> None:
        self.salt = encryption.generate_salt()
        key = encryption.derive_key(self.password, self.salt)
        self.password = Fernet(key).encrypt(self.password.encode()).decode()

    def decrypt(self) -> str:
        key = encryption.derive_key(self.password, self.salt)
        return Fernet(key).decrypt(self.password.encode()).decode()
