from cipherspy.cipher import *


class InvalidAlgorithmException(Exception):
    def __init__(self, algorithm: str) -> None:
        super().__init__(f"Invalid algorithm name {algorithm}")


class PasswordGenerator:
    """
    A strong password generator use multiple cipher algorithms to cipher a given plain text
    """
    def __init__(
            self,
            text: str = None,
            shift: int = 3,
            multiplier: int = 3,
            key_str: str = "secret",
            key_iter: iter = (9, 4, 5, 7),
            algorithm: str = 'playfair'
    ):
        """
        :param text: plain text to be ciphered
        :param shift: number of characters to shift each character (default 3)
        :param multiplier: number of characters to shift each character (default 3)
        :param key_str: cipher key string (default "secret")
        :param key_iter: cipher key matrix (default (9, 4, 5, 7))
        :param algorithm: main cipher algorithm name (default 'playfair')
        """
        self._chars_replacements: dict = {}
        self._text: str = text
        self._shift: int = shift
        self._multiplier: int = multiplier
        self._key_str: str = key_str
        self._key_iter: iter = key_iter
        self._algorithm_name: str = algorithm.lower()
        self._algorithm = self._set_algorithm()
        self._password: str = f'secret{self._text}secret'

    @property
    def text(self) -> str:
        """
        Returns the text to be ciphered into a password
        Eg: ```password = pg.text```
        :return: str: The text to be ciphered into a password
        """
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        """
        Sets the text to be ciphered into a password
        Eg: ```pg.text = 'secret 2024 password'```
        :param text: The text to be ciphered into a password
        :return:
        """
        self._text = text
        self._password: str = f'secret{self._text}secret'

    @property
    def shift(self) -> int:
        """
        Returns the shift value for the cipher algorithm
        Eg: ```shift = pg.shift```
        :return: int: The shift value for the cipher algorithm
        """
        return self._shift

    @shift.setter
    def shift(self, shift: int) -> None:
        """
        Sets the shift value for the cipher algorithm
        Eg: ```pg.shift = 3```
        :param shift: The shift value for the cipher algorithm
        :return:
        """
        self._shift = shift

    @property
    def multiplier(self) -> int:
        """
        Returns the multiplier value for the cipher algorithm
        Eg: ```multiplier = pg.multiplier```
        :return: int: The multiplier value for the cipher algorithm
        """
        return self._multiplier

    @multiplier.setter
    def multiplier(self, multiplier: int) -> None:
        """
        Sets the multiplier value for the cipher algorithm
        Eg: ```pg.multiplier = 3```
        :param multiplier: The multiplier value for the cipher algorithm
        :return:
        """
        self._multiplier = multiplier

    @property
    def key_str(self) -> str:
        """
        Returns the key string for the cipher algorithm
        Eg: ```key_str = pg.key_str```
        :return: str: The key string for the cipher algorithm
        """
        return self._key_str

    @key_str.setter
    def key_str(self, key_str: str) -> None:
        """
        Sets the key string for the cipher algorithm
        Eg: ```pg.key_str = 'secret key'```
        :param key_str: The key string for the cipher algorithm
        :return:
        """
        self._key_str = key_str

    @property
    def key_iter(self) -> iter:
        """
        Returns the key matrix for the cipher algorithm
        Eg: ```key_iter = pg.key_iter```
        :return: iter: The key matrix for the cipher algorithm
        """
        return self._key_iter

    @key_iter.setter
    def key_iter(self, key_iter: iter) -> None:
        """
        Sets the key matrix for the cipher algorithm
        Eg: ```pg.key_iter = (9, 5, 2, 4)```
        :param key_iter: The key matrix for the cipher algorithm
        :return:
        """
        self._key_iter = key_iter

    @property
    def algorithm(self) -> str:
        """
        Returns the main cipher algorithm name
        Eg: ```algorithm = pg.algorithm```
        :return: str: The main cipher algorithm name
        """
        return self._algorithm_name

    @algorithm.setter
    def algorithm(self, algorithm: str) -> None:
        """
        Sets the main cipher algorithm
        Eg: ```pg.algorithm = 'playfair'```
        :param algorithm: The name of the main cipher algorithm
        :return:
        """
        self._algorithm_name = algorithm.lower()
        self._algorithm = self._set_algorithm()

    @property
    def characters_replacements(self) -> dict:
        """
        Returns the dictionary of the characters replacements
        Eg: ```print(pg.characters_replacements)  # {'a': '@1', 'b': '#2'}```
        :return: dict: The dictionary of the characters replacements
        """
        return self._chars_replacements

    def _set_algorithm(self):
        """
        Return new instance of the used algorithm to the given one by it's name
        :return: new algorithm class
        """
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
        """
        Update the main cipher algorithm
        """
        self._algorithm = self._set_algorithm()

    def replace_character(self, char: str, replacement: str) -> None:
        """
        Replace a character with another character or set of characters
        Eg: pg.replace_character('a', '@1')
        :param char: The character to be replaced
        :param replacement: The (character|set of characters) to replace the first one
        :return:
        """
        self._chars_replacements[char[0]] = replacement

    def reset_character(self, char: str) -> None:
        """
        Reset a character to it's original value (remove it's replacement from characters_replacements)
        :param char: The character to be reset to its original value
        :return:
        """
        if char in self._chars_replacements:
            del self._chars_replacements[char]

    def generate_raw_password(self) -> str:
        """
        Generate a raw password string using the given parameters
        :return: str: The generated raw password
        """
        self._update_algorithm_properties()
        return self._algorithm.encrypt(self._password)

    def generate_password(self) -> str:
        """
        Generate a strong password string using the raw password (add another layer of encryption to it)
        :return: str: The generated strong password
        """
        old_algorithm = self._algorithm_name
        self._algorithm_name = 'affine'
        self._update_algorithm_properties()
        self._password = self.generate_raw_password()
        self._algorithm_name = old_algorithm
        self._update_algorithm_properties()
        for char, replacement in self._chars_replacements.items():
            self._password = self._password.replace(char, replacement)
        for char in self._password:
            if char in self._text:
                self._password = self._text.replace(char, char.upper())
        return self._password
