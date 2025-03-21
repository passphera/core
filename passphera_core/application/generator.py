from datetime import datetime, timezone
from uuid import UUID

from passphera_core.entities import Generator
from passphera_core.interfaces import GeneratorRepository


class GetGeneratorUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def execute(self) -> Generator:
        return self.generator_repository.get()
    
    
class GetGeneratorPropertyUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def execute(self, field: str) -> str:
        generator_entity: Generator = self.generator_repository.get()
        return getattr(generator_entity, field)


class UpdateGeneratorPropertyUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def execute(self, field: str, value: str) -> None:
        generator_entity: Generator = self.generator_repository.get()
        setattr(generator_entity, field, value)
        if field == 'algorithm':
            generator_entity.get_algorithm()
        generator_entity.updated_at = datetime.now(timezone.utc)
        self.generator_repository.update(generator_entity)


class AddCharacterReplacementUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def execute(self, character: str, replacement: str) -> None:
        generator_entity: Generator = self.generator_repository.get()
        generator_entity.replace_character(character, replacement)
        generator_entity.updated_at = datetime.now(timezone.utc)
        self.generator_repository.update(generator_entity)


class ResetCharacterReplacementUseCase:
    def __init__(self, generator_repository: GeneratorRepository,):
        self.generator_repository: GeneratorRepository = generator_repository

    def execute(self, character: str) -> None:
        generator_entity: Generator = self.generator_repository.get()
        generator_entity.reset_character(character)
        generator_entity.updated_at = datetime.now(timezone.utc)
        self.generator_repository.update(generator_entity)
