from datetime import datetime, timezone

from passphera_core.entities import Password, Generator
from passphera_core.exceptions import DuplicatePasswordException
from passphera_core.interfaces import PasswordRepository, GeneratorRepository
from passphera_core.utilities import get_password


class GeneratePasswordUseCase:
    def __init__(
            self,
            password_repository: PasswordRepository,
            generator_repository: GeneratorRepository,
    ):
        self.password_repository: PasswordRepository = password_repository
        self.generator_repository: GeneratorRepository = generator_repository

    def execute(self, context: str, text: str) -> Password:
        password_entity: Password = self.password_repository.get_by_context(context)
        if password_entity:
            raise DuplicatePasswordException(password_entity)
        generator_entity: Generator = self.generator_repository.get()
        password: str = generator_entity.generate_password(text)
        password_entity: Password = Password(context=context, text=text, password=password)
        password_entity.encrypt()
        self.password_repository.save(password_entity)
        return password_entity


class GetPasswordUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository: PasswordRepository = password_repository

    def execute(self, context: str) -> Password:
        return get_password(self.password_repository, context)


class UpdatePasswordUseCase:
    def __init__(
            self,
            password_repository: PasswordRepository,
            generator_repository: GeneratorRepository,
    ):
        self.password_repository: PasswordRepository = password_repository
        self.generator_repository: GeneratorRepository = generator_repository

    def execute(self, context: str, text: str) -> None:
        password_entity: Password = get_password(self.password_repository, context)
        generator_entity: Generator = self.generator_repository.get()
        password: str = generator_entity.generate_password(text)
        password_entity.text = text
        password_entity.password = password
        password_entity.updated_at = datetime.now(timezone.utc)
        password_entity.encrypt()
        self.password_repository.update(password_entity)


class DeletePasswordUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository: PasswordRepository = password_repository

    def execute(self, context: str) -> None:
        self.password_repository.delete(get_password(self.password_repository, context))


class ListPasswordsUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository: PasswordRepository = password_repository

    def execute(self) -> list[Password]:
        return self.password_repository.list()


class FlushPasswordsUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository: PasswordRepository = password_repository

    def execute(self) -> None:
        self.password_repository.flush()
