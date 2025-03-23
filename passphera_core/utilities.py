from passphera_core.entities import Password
from passphera_core.exceptions import DuplicatePasswordException
from passphera_core.interfaces import PasswordRepository


def get_password(password_repository: PasswordRepository, context: str) -> Password:
    password_entity: Password = password_repository.get_by_context(context)
    if password_entity:
        raise DuplicatePasswordException(password_entity)
    return password_entity
