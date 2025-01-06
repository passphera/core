from dataclasses import dataclass, field
from uuid import UUID, uuid4

from cipherspy.cipher import *
from cipherspy.cipher.base_cipher import BaseCipherAlgorithm

from passphera_core.utils.exceptions import InvalidAlgorithmException


@dataclass
class GeneratorConfig:
    id: UUID = field(default_factory=uuid4)
    generator_id: UUID = field(default_factory=uuid4)
    shift: int = field(default=3)
    multiplier: int = field(default=3)
    key: str = field(default="hill")
    algorithm: str = field(default="hill")
    prefix: str = field(default="secret")
    postfix: str = field(default="secret")
    characters_replacements: dict[str, str] = field(default_factory=dict[str, str])
    _cipher_registry: dict[str, BaseCipherAlgorithm] = field(default_factory=lambda: {
        'caesar': CaesarCipherAlgorithm,
        'affine': AffineCipherAlgorithm,
        'playfair': PlayfairCipherAlgorithm,
        'hill': HillCipherAlgorithm,
    }, init=False)

    def get_algorithm(self) -> BaseCipherAlgorithm:
        """
        Get the primary algorithm used to cipher the password
        :return: BaseCipherAlgorithm: The primary algorithm used for the cipher
        """
        if self.algorithm.lower() not in self._cipher_registry:
            raise InvalidAlgorithmException(self.algorithm)
        return self._cipher_registry[self.algorithm.lower()]

    def replace_character(self, char: str, replacement: str) -> None:
        """
        Replace a character with another character or set of characters
        Eg: pg.replace_character('a', '@1')
        :param char: The character to be replaced
        :param replacement: The (character|set of characters) to replace the first one
        :return:
        """
        self.characters_replacements[char[0]] = replacement

    def reset_character(self, char: str) -> None:
        """
        Reset a character to it's original value (remove it's replacement from characters_replacements)
        :param char: The character to be reset to its original value
        :return:
        """
        self.characters_replacements.pop(char, None)
