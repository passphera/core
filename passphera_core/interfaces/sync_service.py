from abc import ABC, abstractmethod
from typing import List
from passphera.entities.password import Password

class SyncServiceInterface(ABC):
    @abstractmethod
    def fetch_passwords(self, user_id: str) -> List[Password]:
        pass

    @abstractmethod
    def upload_passwords(self, user_id: str, passwords: List[Password]):
        pass
