from passphera_core.entities import Password, Generator
from passphera_core.exceptions import DuplicatePasswordException
from passphera_core.interfaces import VaultRepository, GeneratorRepository
from passphera_core.utilities import generate_password, get_password


class GeneratePasswordUseCase:
    def __init__(
            self,
            password_repository: VaultRepository,
            generator_repository: GeneratorRepository,
    ):
        self.password_repository: VaultRepository = password_repository
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self, context: str, text: str) -> Password:
        password_entity: Password = self.password_repository.get(context)
        if password_entity:
            raise DuplicatePasswordException(password_entity)
        password_entity: Password = Password(context=context, text=text)
        generator_entity: Generator = self.generator_repository.get()
        generate_password(password_entity, generator_entity)
        self.password_repository.save(password_entity)
        return password_entity


class GetPasswordUseCase:
    def __init__(self, password_repository: VaultRepository):
        self.password_repository: VaultRepository = password_repository

    def __call__(self, context: str) -> Password:
        return get_password(self.password_repository, context)


class UpdatePasswordUseCase:
    def __init__(
            self,
            password_repository: VaultRepository,
            generator_repository: GeneratorRepository,
    ):
        self.password_repository: VaultRepository = password_repository
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self, context: str, text: str) -> Password:
        password_entity: Password = get_password(self.password_repository, context)
        generator_entity: Generator = self.generator_repository.get()
        generate_password(password_entity, generator_entity)
        self.password_repository.update(password_entity)
        return password_entity


class DeletePasswordUseCase:
    def __init__(self, password_repository: VaultRepository):
        self.password_repository: VaultRepository = password_repository

    def __call__(self, context: str) -> None:
        self.password_repository.delete(get_password(self.password_repository, context))


class ListPasswordsUseCase:
    def __init__(self, password_repository: VaultRepository):
        self.password_repository: VaultRepository = password_repository

    def __call__(self) -> list[Password]:
        return self.password_repository.list()


class FlushPasswordsUseCase:
    def __init__(self, password_repository: VaultRepository):
        self.password_repository: VaultRepository = password_repository

    def __call__(self) -> None:
        self.password_repository.flush()
