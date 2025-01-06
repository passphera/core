from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime

from passphera_core.entities.generator import Generator
from passphera_core.entities.password import Password


@dataclass
class User:
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    username: str = field(default_factory=str)
    email: str = field(default_factory=str)
    password: str = field(default_factory=str)
    generator: Generator = field(default_factory=Generator)
    passwords: list[Password] = field(default_factory=list[Password])
