from datetime import datetime, timezone

from passphera_core.entities import Password, Generator
from passphera_core.exceptions import DuplicatePasswordException
from passphera_core.interfaces import VaultRepository


def generate_password(entity: Password, generator: Generator) -> None:
    entity.text = entity.text
    entity.context = entity.context
    entity.password = generator.generate_password(entity.text)
    entity.updated_at = datetime.now(timezone.utc)
    entity.encrypt()


def get_password(password_repository: VaultRepository, context: str) -> Password:
    password_entity: Password = password_repository.get(context)
    if password_entity:
        raise DuplicatePasswordException(password_entity)
    return password_entity
