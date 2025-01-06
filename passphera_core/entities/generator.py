from dataclasses import dataclass, field

from cipherspy.cipher import *
from cipherspy.cipher.base_cipher import BaseCipherAlgorithm

from passphera_core.exceptions import InvalidAlgorithmException


@dataclass
class GeneratorConfig:
    shift: int = 3
    multiplier: int = 3
    key: str = "hill"
    algorithm: str = 'hill'
    prefix: str = 'secret'
    postfix: str = 'secret'
    characters_replacements: dict[str, str] = field(default_factory=dict)


@dataclass
class Generator:
    config: GeneratorConfig
    _cipher_registry: dict[str, BaseCipherAlgorithm] = field(default_factory=lambda: {
        'caesar': CaesarCipherAlgorithm,
        'affine': AffineCipherAlgorithm,
        'playfair': PlayfairCipherAlgorithm,
        'hill': HillCipherAlgorithm,
    }, init=False)

    def _get_algorithm(self) -> BaseCipherAlgorithm:
        if self.config.algorithm.lower() not in self._cipher_registry:
            raise InvalidAlgorithmException(self.config.algorithm)
        return self._cipher_registry[self.config.algorithm.lower()]

    def replace_character(self, char: str, replacement: str) -> None:
        """
        Replace a character with another character or set of characters
        Eg: pg.replace_character('a', '@1')
        :param char: The character to be replaced
        :param replacement: The (character|set of characters) to replace the first one
        :return:
        """
        self.config.characters_replacements[char[0]] = replacement

    def reset_character(self, char: str) -> None:
        """
        Reset a character to it's original value (remove it's replacement from characters_replacements)
        :param char: The character to be reset to its original value
        :return:
        """
        self.config.characters_replacements.pop(char, None)

    def apply_replacements(self, password: str) -> str:
        translation_table = str.maketrans(self.config.characters_replacements)
        return password.translate(translation_table)

    def generate_password(self, text: str) -> str:
        """
        Generate a strong password string using the raw password (add another layer of encryption to it)
        :return: str: The generated strong password
        """
        affine = AffineCipherAlgorithm(self.config.shift, self.config.multiplier)
        intermediate = affine.encrypt(f"{self.config.prefix}{text}{self.config.postfix}")
        main_algorithm = self._get_algorithm()
        password = main_algorithm.encrypt(intermediate)
        password = self.apply_replacements(password)
        return ''.join(c.upper() if c in text else c for c in password)


# class Generator:
#     """
#     A strong password generator use multiple cipher algorithms to cipher a given plain text
#     """
#
#     _cipher_registry = {
#         'caesar': CaesarCipherAlgorithm,
#         'affine': AffineCipherAlgorithm,
#         'playfair': PlayfairCipherAlgorithm,
#         'hill': HillCipherAlgorithm,
#     }
#
#     def __init__(
#             self,
#             shift: int = 3,
#             multiplier: int = 3,
#             key: str = "hill",
#             algorithm: str = 'hill',
#             prefix: str = 'secret',
#             postfix: str = 'secret',
#             characters_replacements: dict = None,
#     ):
#         """
#         :param shift: number of characters to shift each character (default 3)
#         :param multiplier: number of characters to shift each character (default 3)
#         :param key: cipher key string (default "secret")
#         :param algorithm: main cipher algorithm name (default 'playfair')
#         :param characters_replacements: replace characters with the given values (default {})
#         :param text: plain text to be ciphered
#         """
#         if characters_replacements is None:
#             characters_replacements = {}
#         self._shift: int = shift
#         self._multiplier: int = multiplier
#         self._key: str = key
#         self._algorithm: BaseCipherAlgorithm = self._set_algorithm(algorithm.lower())
#         self._prefix: str = prefix
#         self._postfix: str = postfix
#         self._characters_replacements: dict = characters_replacements
#
#     @property
#     def shift(self) -> int:
#         """
#         Returns the shift value for the cipher algorithm
#         Eg: ```shift = pg.shift```
#         :return: int: The shift value for the cipher algorithm
#         """
#         return self._shift
#
#     @shift.setter
#     def shift(self, shift: int) -> None:
#         """
#         Sets the shift value for the cipher algorithm
#         Eg: ```pg.shift = 3```
#         :param shift: The shift value for the cipher algorithm
#         :return:
#         """
#         self._shift = shift
#
#     @property
#     def multiplier(self) -> int:
#         """
#         Returns the multiplier value for the cipher algorithm
#         Eg: ```multiplier = pg.multiplier```
#         :return: int: The multiplier value for the cipher algorithm
#         """
#         return self._multiplier
#
#     @multiplier.setter
#     def multiplier(self, multiplier: int) -> None:
#         """
#         Sets the multiplier value for the cipher algorithm
#         Eg: ```pg.multiplier = 3```
#         :param multiplier: The multiplier value for the cipher algorithm
#         :return:
#         """
#         self._multiplier = multiplier
#
#     @property
#     def key(self) -> str:
#         """
#         Returns the key string for the cipher algorithm
#         Eg: ```key = pg.key```
#         :return: str: The key string for the cipher algorithm
#         """
#         return self._key
#
#     @key.setter
#     def key(self, key: str) -> None:
#         """
#         Sets the key string for the cipher algorithm
#         Eg: ```pg.key = 'secret key'```
#         :param key: The key string for the cipher algorithm
#         :return:
#         """
#         self._key = key
#
#     @property
#     def prefix(self) -> str:
#         """
#         Returns the prefix string for the cipher algorithm
#         Eg: ```prefix = pg.prefix```
#         :return: str: The prefix string for the cipher algorithm
#         """
#         return self._prefix
#
#     @prefix.setter
#     def prefix(self, prefix: str):
#         """
#         Sets the prefix string for the cipher algorithm
#         Eg: ```pg.prefix = 'something'```
#         :param prefix: The string for the cipher algorithm
#         :return:
#         """
#         self._prefix = prefix
#
#     @property
#     def postfix(self) -> str:
#         """
#         Returns the postfix string for the cipher algorithm
#         Eg: ```postfix = pg.postfix```
#         :return: str: The postfix string for the cipher algorithm
#         """
#         return self._postfix
#
#     @postfix.setter
#     def postfix(self, postfix: str):
#         """
#         Sets the postfix string for the cipher algorithm
#         Eg: ```pg.postfix = 'something'```
#         :param postfix: The string for the cipher algorithm
#         :return:
#         """
#         self._postfix = postfix
#
#     @property
#     def algorithm(self) -> str:
#         """
#         Returns the main cipher algorithm name
#         Eg: ```algorithm = pg.algorithm```
#         :return: str: The main cipher algorithm name
#         """
#         return self._algorithm.name
#
#     @algorithm.setter
#     def algorithm(self, algorithm: str) -> None:
#         """
#         Sets the main cipher algorithm
#         Eg: ```pg.algorithm = 'playfair'```
#         :param algorithm: The name of the main cipher algorithm
#         :return:
#         """
#         self._algorithm = self._set_algorithm(algorithm.lower())
#
#     @property
#     def characters_replacements(self) -> dict:
#         """
#         Returns the dictionary of the characters replacements
#         Eg: ```print(pg.characters_replacements)  # {'a': '@1', 'b': '#2'}```
#         :return: dict: The dictionary of the characters replacements
#         """
#         return self._characters_replacements
#
#     def _set_algorithm(self, algorithm_name):
#         """
#         Return new instance of the used algorithm to the given one by it's name
#         :return: new algorithm class
#         """
#         if algorithm_name not in self._cipher_registry:
#             raise InvalidAlgorithmException(algorithm_name)
#         return self._cipher_registry[algorithm_name]
#
#     def replace_character(self, char: str, replacement: str) -> None:
#         """
#         Replace a character with another character or set of characters
#         Eg: pg.replace_character('a', '@1')
#         :param char: The character to be replaced
#         :param replacement: The (character|set of characters) to replace the first one
#         :return:
#         """
#         self._characters_replacements[char[0]] = replacement
#
#     def reset_character(self, char: str) -> None:
#         """
#         Reset a character to it's original value (remove it's replacement from characters_replacements)
#         :param char: The character to be reset to its original value
#         :return:
#         """
#         if char in self._characters_replacements:
#             del self._characters_replacements[char]
#
#     def apply_replacements(self, password: str) -> str:
#         translation_table = str.maketrans(self._characters_replacements)
#         return password.translate(translation_table)
#
#     def generate_raw_password(self, text: str) -> str:
#         """
#         Generate a raw password string using the given parameters
#         :return: str: The generated raw password
#         """
#         return self._algorithm.encrypt(f"{self._prefix}{text}{self._postfix}")
#
#     def generate_password(self, text: str) -> str:
#         """
#         Generate a strong password string using the raw password (add another layer of encryption to it)
#         :return: str: The generated strong password
#         """
#         old_algorithm = self._algorithm
#         self._algorithm = AffineCipherAlgorithm(self._shift, self._multiplier)
#         password = self.generate_raw_password(text)
#         self._algorithm = old_algorithm
#         password = self.generate_raw_password(password)
#         password = self.apply_replacements(password)
#         for char in password:
#             if char in text:
#                 password = password.replace(char, char.upper())
#         return password
