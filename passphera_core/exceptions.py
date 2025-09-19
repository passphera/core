class PasswordNotFoundException(Exception):
    def __init__(self) -> None:
        super().__init__("Password not found")


class DuplicatePasswordException(Exception):
    def __init__(self, password) -> None:
        self.password = password
        message = self._build_message(password)
        super().__init__(message)

    @staticmethod
    def _build_message(password) -> str:
        if hasattr(password, 'context') and password.context:
            return f"Password for context '{password.context}' already exists"
        return "Duplicate password detected"


class InvalidPropertyNameException(Exception):
    def __init__(self, property_name: str) -> None:
        self.property_name = property_name
        super().__init__(f"Invalid property name '{property_name}'")
