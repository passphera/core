from passphera_core.entities import Generator
from passphera_core.interfaces import GeneratorRepository


class GetGeneratorUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self) -> Generator:
        return self.generator_repository.get()


class GetPropertiesUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self) -> dict:
        return self.generator_repository.get().get_properties()


class SetPropertyUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self, prop: str, value: str) -> Generator:
        generator_entity: Generator = self.generator_repository.get()
        generator_entity.set_property(prop, value)
        self.generator_repository.update(generator_entity)
        return generator_entity


class ResetPropertyUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self, prop: str) -> Generator:
        generator_entity: Generator = self.generator_repository.get()
        generator_entity.reset_property(prop)
        self.generator_repository.update(generator_entity)
        return generator_entity


class GetCharacterReplacementUseCase:
    def __init__(self, generator_repository: GeneratorRepository):
        self.generator_repository: GeneratorRepository = generator_repository

    def __call__(self, character: str) -> str:
        return self.generator_repository.get().get_character_replacement(character)


class SetCharacterReplacementUseCase:
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
