from datetime import datetime, timezone
from uuid import UUID

from passphera_core.entities import Password, Generator, User
from passphera_core.exceptions import EntityNotFoundException
from passphera_core.interfaces import PasswordRepository, GeneratorRepository, UserRepository


class GeneratePasswordUseCase:
    def __init__(
            self,
            password_repository: PasswordRepository,
            generator_repository: GeneratorRepository,
            user_repository: UserRepository
    ):
        self.password_repository: PasswordRepository = password_repository
        self.generator_repository: GeneratorRepository = generator_repository
        self.user_repository: UserRepository = user_repository

    def execute(self, user_id: UUID, context: str, text: str) -> Password:
        user_entity: User = self.user_repository.find_by_id(user_id)
        generator_entity: Generator = self.generator_repository.find_by_id(user_entity.generator)
        password: str = generator_entity.generate_password(text)
        password_entity: Password = Password(user_id=user_id, context=context, text=text, password=password)
        password_entity.encrypt()
        self.password_repository.save(password_entity)
        user_entity.add_password(password_entity.id)
        self.user_repository.update(user_entity)
        return password_entity


class GetPasswordByIdUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository: PasswordRepository = password_repository

    def execute(self, password_id: UUID) -> Password:
        password_entity: Password = self.password_repository.find_by_id(password_id)
        if not password_entity:
            raise EntityNotFoundException(password_entity)
        return password_entity


class GetPasswordByContextUseCase:
    def __init__(self, password_repository: PasswordRepository, user_repository: UserRepository):
        self.password_repository: PasswordRepository = password_repository
        self.user_repository: UserRepository = user_repository

    def execute(self, user_id: UUID, context: str) -> Password:
        user_entity: User = self.user_repository.find_by_id(user_id)
        for password_id in user_entity.passwords:
            password_entity: Password = self.password_repository.find_by_id(password_id)
            if password_entity.context == context:
                return password_entity
        raise EntityNotFoundException(Password())


class UpdatePasswordUseCase:
    def __init__(
            self,
            password_repository: PasswordRepository,
            generator_repository: GeneratorRepository,
            user_repository: UserRepository
    ):
        self.password_repository: PasswordRepository = password_repository
        self.generator_repository: GeneratorRepository = generator_repository
        self.user_repository: UserRepository = user_repository

    def execute(self, user_id: UUID, context: str, text: str) -> Password:
        user_entity: User = self.user_repository.find_by_id(user_id)
        generator_entity: Generator = self.generator_repository.find_by_id(user_entity.generator)
        for password_id in user_entity.passwords:
            password_entity: Password = self.password_repository.find_by_id(password_id)
            if password_entity.context == context:
                password_entity.password = generator_entity.generate_password(text)
                password_entity.encrypt()
                password_entity.updated_at = datetime.now(timezone.utc)
                self.password_repository.update(password_entity)
                return password_entity
        raise EntityNotFoundException(Password())


class DeletePasswordUseCase:
    def __init__(self, password_repository: PasswordRepository, user_repository: UserRepository):
        self.password_repository: PasswordRepository = password_repository
        self.user_repository: UserRepository = user_repository

    def execute(self, user_id: UUID, password_id: UUID) -> None:
        self.password_repository.delete(password_id)
        user_entity: User = self.user_repository.find_by_id(user_id)
        user_entity.delete_password(password_id)
        self.user_repository.update(user_entity)


class GetAllUserPasswordsUseCase:
    def __init__(self, password_repository: PasswordRepository, user_repository: UserRepository):
        self.password_repository: PasswordRepository = password_repository
        self.user_repository: UserRepository = user_repository

    def execute(self, user_id: UUID) -> list[Password]:
        user_entity: User = self.user_repository.find_by_id(user_id)
        passwords: list[Password] = []
        for password_id in user_entity.passwords:
            password_entity: Password = self.password_repository.find_by_id(password_id)
            passwords.append(password_entity)
        return passwords


class DeleteAllUserPasswordsUseCase:
    def __init__(self, password_repository: PasswordRepository, user_repository: UserRepository):
        self.password_repository: PasswordRepository = password_repository
        self.user_repository: UserRepository = user_repository

    def execute(self, user_id: UUID) -> None:
        user_entity: User = self.user_repository.find_by_id(user_id)
        for password_id in user_entity.passwords:
            self.password_repository.delete(password_id)
            user_entity.delete_password(password_id)
        self.user_repository.update(user_entity)
