from uuid import UUID

from passphera_core.entities import Password, Generator, User
from passphera_core.interfaces import PasswordRepository, UserRepository


class GeneratePasswordUseCase:
    def __init__(self, password_repository: PasswordRepository, user_repository: UserRepository):
        self.password_repository: PasswordRepository = password_repository
        self.user_repository: UserRepository = user_repository

    def execute(self, user_id: UUID, context: str, text: str) -> Password:
        user_entity: User = self.user_repository.find_by_id(user_id)
        generator_entity: Generator = user_entity.generator
        password = generator_entity.generate_password(text)
        password_entity = Password(user_id=user_id, context=context, text=text, password=password)
        password_entity.encrypt()
        self.password_repository.save(password_entity)
        user_entity.add_password(password_entity)
        self.user_repository.update(user_entity)
        return password_entity


class GetPasswordUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository: PasswordRepository = password_repository

    def execute(self, context: str) -> Password:
        return self.password_repository.find_by_context(context)


class UpdatePasswordUseCase:
    def __init__(self, password_repository: PasswordRepository, user_repository: UserRepository):
        self.password_repository = password_repository
        self.user_repository = user_repository

    def execute(self, user_id: UUID, context: str, text: str) -> Password:
        user_entity: User = self.user_repository.find_by_id(user_id)
        generator_entity: Generator = user_entity.generator
        password_entity = self.password_repository.find_by_context(context)
        password_entity.password = generator_entity.generate_password(text)
        password_entity.encrypt()
        self.password_repository.update(password_entity)
        user_entity.update_password(password_entity)
        self.user_repository.update(user_entity)
        return password_entity


class DeletePasswordUseCase:
    def __init__(self, password_repository: PasswordRepository, user_repository: UserRepository):
        self.password_repository = password_repository
        self.user_repository = user_repository

    def execute(self, user_id: UUID, password_id: UUID) -> None:
        user_entity: User = self.user_repository.find_by_id(user_id)
        password_entity: Password = self.password_repository.find_by_id(password_id)
        self.user_repository.delete(password_id)
        user_entity.delete_password(password_entity)
        self.user_repository.update(user_entity)


class GetAllUserPasswordsUseCase:
    def __init__(self, password_repository: PasswordRepository, user_repository: UserRepository):
        self.password_repository = password_repository
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> list[Password]:
        user_entity: User = self.user_repository.find_by_id(user_id)
        passwords: list[Password] = []
        for password in user_entity.passwords:
            passwords.append(password)
        return passwords


class DeleteAllUserPasswordsUseCase:
    def __init__(self, password_repository: PasswordRepository, user_repository: UserRepository):
        self.password_repository = password_repository
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> None:
        user_entity: User = self.user_repository.find_by_id(user_id)
        for password in user_entity.passwords:
            self.password_repository.delete(password.id)
            user_entity.delete_password(password)
            self.user_repository.update(user_entity)


class SyncUserPasswordsUseCase:
    def __init__(self, password_repository: PasswordRepository, user_repository: UserRepository):
        self.password_repository = password_repository
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> None:
        pass
