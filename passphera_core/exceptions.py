from typing import Union, Literal

from passphera_core.entities import Password, Generator, User


class InvalidAlgorithmException(Exception):
    def __init__(self, algorithm: str) -> None:
        self.algorithm = algorithm
        super().__init__(f"Invalid algorithm: '{algorithm}'")


class EntityNotFoundException(Exception):
    def __init__(self, entity: Union[Password, Generator, User]) -> None:
        self.entity = entity
        entity_type = entity.__class__.__name__
        super().__init__(f"{entity_type} not found")


class DuplicateEntityException(Exception):
    def __init__(
            self,
            entity: Union[Password, User],
            duplicate_field: Literal['context', 'email', 'username'] = None
    ) -> None:
        self.entity = entity
        self.duplicate_field = duplicate_field
        message = self._build_message(entity, duplicate_field)
        super().__init__(message)

    def _build_message(self, entity: Union[Password, User], duplicate_field: str | None) -> str:
        if isinstance(entity, Password):
            return self._build_password_message(entity)
        elif isinstance(entity, User):
            return self._build_user_message(entity, duplicate_field)
        return "Duplicate entity detected"

    @staticmethod
    def _build_password_message(password: Password) -> str:
        if hasattr(password, 'context') and password.context:
            return f"Password for context '{password.context}' already exists"
        return "Duplicate password detected"

    @staticmethod
    def _build_user_message(user: User, duplicate_field: str) -> str:
        if duplicate_field == 'email':
            return f"User with email '{user.email}' already exists"
        elif duplicate_field == 'username':
            return f"User with username '{user.username}' already exists"
        return "Duplicate user detected"
