from uuid import UUID

from passphera_core.entities import Generator, User
from passphera_core.interfaces import GeneratorRepository, GeneratorConfigRepository, UserRepository


class SyncGeneratorUseCase:
    def __init__(self, generator_repository: GeneratorRepository, user_repository: UserRepository):
        self.generator_repository = generator_repository
        self.user_repository = user_repository

    def execute(self):
        pass
