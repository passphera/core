from uuid import UUID

from passphera_core.entities import Password
from passphera_core.interfaces import PasswordRepository


class GeneratePasswordUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository = password_repository

    def execute(self, user_id: UUID, context: str, text: str) -> Password:
        user_entity = self.database.get_user(user_id)
        generator_entity = user_entity.generator
        password = generator_entity.generate_password(text)
        password_entity = Password(user_id=user_id, context=context, text=text, password=password)
        password_entity.encrypt()
        self.database.save_password(password_entity)
        return password_entity
