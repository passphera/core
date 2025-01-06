from abc import ABC, abstractmethod
from passphera.entities.user import User

class DatabaseInterface(ABC):
    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    def save_user(self, user: User):
        pass
