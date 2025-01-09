from abc import ABC, abstractmethod
from uuid import UUID

from passphera_core.entities import Password, Generator, GeneratorConfig, User


class PasswordRepository(ABC):
    @abstractmethod
    def save(self, password: Password) -> None:
        pass

    @abstractmethod
    def update(self, password: Password) -> None:
        pass

    @abstractmethod
    def delete(self, password_id: UUID) -> None:
        pass

    @abstractmethod
    def find_by_id(self, password_id: UUID) -> Password:
        pass


class GeneratorRepository(ABC):
    @abstractmethod
    def save(self, generator: Generator) -> None:
        pass

    @abstractmethod
    def update(self, generator: Generator) -> None:
        pass

    @abstractmethod
    def delete(self, generator_id: UUID) -> None:
        pass

    @abstractmethod
    def find_by_id(self, generator_id: UUID) -> Generator:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: UUID) -> Generator:
        pass


class GeneratorConfigRepository(ABC):
    @abstractmethod
    def save(self, generator_config: GeneratorConfig) -> None:
        pass

    @abstractmethod
    def update(self, generator_config: GeneratorConfig) -> None:
        pass

    @abstractmethod
    def delete(self, generator_config_id: UUID) -> None:
        pass

    @abstractmethod
    def find_by_id(self, generator_config_id: UUID) -> GeneratorConfig:
        pass

    @abstractmethod
    def find_by_generator_id(self, generator_id: UUID) -> GeneratorConfig:
        pass


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        pass
