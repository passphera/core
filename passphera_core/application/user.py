from uuid import UUID

from passphera_core.entities import User
from passphera_core.interfaces import UserRepository


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self):
        pass


class AuthenticateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self):
        pass
