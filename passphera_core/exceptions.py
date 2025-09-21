class InvalidPropertyNameException(Exception):
    def __init__(self, property_name: str) -> None:
        self.property_name = property_name
        super().__init__(f"Invalid property name '{property_name}'")
