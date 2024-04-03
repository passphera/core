from password_generator import PasswordGenerator


class Generator:
    def __init__(self):
        self._generator = PasswordGenerator()

    def generate_password(self, text, key, shift):
        self._generator.key = key
        self._generator.shift = shift
        self._generator.text = f'password{text}password'
        self._generator.algorithm = 'caesar'
        self._generator.text = self._generator.generate_raw_password()
        self._generator.algorithm = 'playfair'
        return self._generator.generate_password()

    def change_shift(self, shift):
        self._generator.shift = shift

    def replace_character(self, character, replacement):
        self._generator.replace_character(character, replacement)

    def reset_character(self, character):
        self._generator.reset_character(character)
