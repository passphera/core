from datetime import datetime, timezone
from uuid import UUID

from passphera_core.entities import Generator, GeneratorConfig
from passphera_core.interfaces import GeneratorRepository, GeneratorConfigRepository


class GetGeneratorUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def execute(self, user_id: UUID) -> Generator:
        return self.generator_repository.find_by_user_id(user_id)
    
    
class GetGeneratorConfigPropertyUseCase:
    def __init__(self, generator_repository: GeneratorRepository, generator_config_repository: GeneratorConfigRepository):
        self.generator_repository: GeneratorRepository = generator_repository
        self.generator_config_repository: GeneratorConfigRepository = generator_config_repository

    def execute(self, user_id: UUID, field: str) -> str:
        generator_entity: Generator = self.generator_repository.find_by_user_id(user_id)
        generator_config_entity: GeneratorConfig = self.generator_config_repository.find_by_generator_id(generator_entity.id)
        return getattr(generator_config_entity, field)


class UpdateGeneratorConfigUseCase:
    def __init__(
            self,
            generator_repository: GeneratorRepository,
            generator_config_repository: GeneratorConfigRepository,
    ):
        self.generator_repository: GeneratorRepository = generator_repository
        self.generator_config_repository: GeneratorConfigRepository = generator_config_repository

    def execute(self, user_id: UUID, field: str, value: str) -> None:
        generator_entity: Generator = self.generator_repository.find_by_user_id(user_id)
        generator_config_entity: GeneratorConfig = self.generator_config_repository.find_by_generator_id(generator_entity.id)
        setattr(generator_config_entity, field, value)
        if field == 'algorithm':
            generator_config_entity.get_algorithm()
        generator_config_entity.updated_at = datetime.now(timezone.utc)
        self.generator_config_repository.update(generator_config_entity)



class AddCharacterReplacementUseCase:
    def __init__(
            self,
            generator_repository: GeneratorRepository,
            generator_config_repository: GeneratorConfigRepository,
    ):
        self.generator_repository: GeneratorRepository = generator_repository
        self.generator_config_repository: GeneratorConfigRepository = generator_config_repository

    def execute(self, user_id: UUID, character: str, replacement: str) -> None:
        generator_entity: Generator = self.generator_repository.find_by_user_id(user_id)
        generator_config_entity: GeneratorConfig = self.generator_config_repository.find_by_generator_id(generator_entity.id)
        generator_config_entity.replace_character(character, replacement)
        generator_config_entity.updated_at = datetime.now(timezone.utc)
        self.generator_config_repository.update(generator_config_entity)


class ResetCharacterReplacementUseCase:
    def __init__(
            self,
            generator_repository: GeneratorRepository,
            generator_config_repository: GeneratorConfigRepository,
    ):
        self.generator_repository: GeneratorRepository = generator_repository
        self.generator_config_repository: GeneratorConfigRepository = generator_config_repository

    def execute(self, user_id: UUID, character: str) -> None:
        generator_entity: Generator = self.generator_repository.find_by_user_id(user_id)
        generator_config_entity: GeneratorConfig = self.generator_config_repository.find_by_generator_id(generator_entity.id)
        generator_config_entity.reset_character(character)
        generator_config_entity.updated_at = datetime.now(timezone.utc)
        self.generator_config_repository.update(generator_config_entity)
