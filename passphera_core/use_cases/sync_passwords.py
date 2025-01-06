from passphera_core.interfaces.sync_service import SyncServiceInterface
from passphera_core.interfaces.database import DatabaseInterface

class SyncPasswordsUseCase:
    def __init__(self, database: DatabaseInterface, sync_service: SyncServiceInterface):
        self.database = database
        self.sync_service = sync_service

    def execute(self, user_id: str):
        user = self.database.get_user(user_id)
        remote_passwords = self.sync_service.fetch_passwords(user_id)
        # Example merge logic
        for remote_password in remote_passwords:
            if remote_password.password_id not in [p.password_id for p in user.passwords]:
                user.add_password(remote_password)
        self.sync_service.upload_passwords(user_id, user.passwords)
        self.database.save_user(user)
