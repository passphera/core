class Password:
    def __init__(self, text: str, context: str, salt: bytes = None):
        self.id = uuid4()
        self.text = text
        self.context = context
        self.salt = salt
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def update_password(self, new_text: str):
        self.text = new_text
        self.updated_at = datetime.now(timezone.utc)
