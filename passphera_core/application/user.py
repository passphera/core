from uuid import UUID

from passphera_core.entities import User, Generator
from passphera_core.exceptions import DuplicateEntityException
from passphera_core.interfaces import UserRepository, GeneratorRepository


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository, generator_repository: GeneratorRepository):
        self.user_repository: UserRepository = user_repository
        self.generator_repository: GeneratorRepository = generator_repository

    def execute(self, user: User) -> User:
        if self.user_repository.find_by_email(user.email):
            raise DuplicateEntityException(user, 'email')
        if self.user_repository.find_by_username(user.username):
            raise DuplicateEntityException(user, 'username')
        user_entity: User = User(**user.__dict__)
        generator_entity: Generator = Generator(user_id=user_entity.id)
        self.generator_repository.save(generator_entity)
        user_entity.generator = generator_entity.id
        self.user_repository.save(user_entity)
        return user_entity


class GetUserByIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository: UserRepository = user_repository

    def execute(self, id: UUID) -> User:
        user = self.user_repository.find_by_id(id)
        if not user:
            raise ValueError(f'User not found')
        return user


class GetUserByUsernameUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, username: str) -> User:
        user = self.user_repository.find_by_username(username)
        if not user:
            raise ValueError(f'User not found')
        return user


class GetUserByEmailUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str) -> User:
        user = self.user_repository.find_by_email(email)
        if not user:
            raise ValueError(f'User not found')
        return user
