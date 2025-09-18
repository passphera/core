from passphera_core.entities import Generator
from passphera_core.interfaces import GeneratorRepository


class GetGeneratorUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self) -> Generator:
        return self.generator_repository.get()
    
    
class GetGeneratorPropertyUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self, field: str) -> str:
        generator_entity: Generator = self.generator_repository.get()
        return getattr(generator_entity, field)


class UpdateGeneratorPropertyUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self, field: str, value: str) -> str:
        generator_entity: Generator = self.generator_repository.get()
        generator_entity.update_property(field, value)
        self.generator_repository.update(generator_entity)
        return getattr(generator_entity, field)


class AddCharacterReplacementUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self, character: str, replacement: str) -> Generator:
        generator_entity: Generator = self.generator_repository.get()
        generator_entity.replace_character(character, replacement)
        self.generator_repository.update(generator_entity)
        return generator_entity


class ResetCharacterReplacementUseCase:
    def __init__(self, generator_repository: GeneratorRepository,):
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self, character: str) -> Generator:
        generator_entity: Generator = self.generator_repository.get()
        generator_entity.reset_character(character)
        self.generator_repository.update(generator_entity)
        return generator_entity
