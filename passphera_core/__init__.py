from cipherspy.cipher import *


class InvalidAlgorithmException(Exception):
    def __init__(self, algorithm: str) -> None:
        super().__init__(f"Invalid algorithm name {algorithm}")


class PasswordGenerator:
    def __init__(
            self,
            text: str = None,
            shift: int = 3,
            multiplier: int = 3,
            key_str: str = "secret",
            key_iter: iter = (9, 4, 5, 7),
            algorithm: str = 'playfair'
    ):
        self._char_replacements: dict = {}
        self._text: str = text
        self._shift: int = shift
        self._multiplier: int = multiplier
        self._key_str: str = key_str
        self._key_iter: iter = key_iter
        self._algorithm_name: str = algorithm.lower()
        self._algorithm = self._set_algorithm()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    @property
    def shift(self) -> int:
        return self._shift

    @shift.setter
    def shift(self, shift: int) -> None:
        self._shift = shift

    @property
    def multiplier(self) -> int:
        return self._multiplier

    @multiplier.setter
    def multiplier(self, multiplier: int) -> None:
        self._multiplier = multiplier

    @property
    def key_str(self) -> str:
        return self._key_str

    @key_str.setter
    def key_str(self, key_str: str) -> None:
        self._key_str = key_str

    @property
    def key_iter(self) -> iter:
        return self._key_iter

    @key_iter.setter
    def key_iter(self, key_iter: iter) -> None:
        self._key_iter = key_iter

    @property
    def algorithm(self) -> str:
        return self._algorithm_name

    @algorithm.setter
    def algorithm(self, algorithm: str) -> None:
        self._algorithm_name = algorithm.lower()
        self._algorithm = self._set_algorithm()

    @property
    def character_replacements(self) -> dict:
        return self._char_replacements

    def _set_algorithm(self):
        match self._algorithm_name:
            case 'caesar':
                return CaesarCipher(self._shift)
            case 'affine':
                return AffineCipher(self._multiplier, self._shift)
            case 'playfair':
                return PlayfairCipher(self._key_str)
            case 'hill':
                return HillCipher(self._key_iter)
            case _:
                raise InvalidAlgorithmException(self._algorithm_name)

    def _update_algorithm_properties(self) -> None:
        self._algorithm = self._set_algorithm()

    def _custom_cipher(self, password: str) -> str:
        for char, replacement in self._char_replacements.items():
            password = password.replace(char, replacement)
        for i in range(len(password)):
            if password[i] in self._text:
                password = password.replace(password[i], password[i].upper())
        return password

    def replace_character(self, char: str, replacement: str) -> None:
        self._char_replacements[char[0]] = replacement

    def reset_character(self, char: str) -> None:
        if char in self._char_replacements:
            del self._char_replacements[char]

    def generate_raw_password(self) -> str:
        self._update_algorithm_properties()
        return self._algorithm.encrypt(self._text)

    def generate_password(self) -> str:
        return self._custom_cipher(self.generate_raw_password())
