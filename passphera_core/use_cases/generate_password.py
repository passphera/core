from passphera_core.entities.password import Password
from passphera_core.interfaces.database import DatabaseInterface

class GeneratePasswordUseCase:
    def __init__(self, database: DatabaseInterface):
        self.database = database

    def execute(self, user_id: str, context: str, text: str, salt: str) -> Password:
        user = self.database.get_user(user_id)
        generator = user.generator
        ciphered_password = generator.generate(text, salt)
        password = Password(context, text, salt, ciphered_password)
        user.add_password(password)
        self.database.save_user(user)
        return password
