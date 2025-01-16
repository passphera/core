from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from cryptography.fernet import Fernet

from cipherspy.cipher import *
from cipherspy.exceptions import InvalidAlgorithmException
from cipherspy.utilities import generate_salt, derive_key


@dataclass
class Password:
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    context: str = field(default_factory=str)
    text: str = field(default_factory=str)
    password: str = field(default_factory=str)
    salt: bytes = field(default_factory=lambda: bytes)

    def encrypt(self) -> None:
        self.salt = generate_salt()
        key = derive_key(self.password, self.salt)
        self.password = Fernet(key).encrypt(self.password.encode()).decode()

    def decrypt(self) -> str:
        key = derive_key(self.password, self.salt)
        return Fernet(key).decrypt(self.password.encode()).decode()


@dataclass
class Generator:
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
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
        Reset a character to its original value (remove its replacement from characters_replacements)
        :param char: The character to be reset to its original value
        :return:
        """
        self.characters_replacements.pop(char, None)

    def apply_replacements(self, password: str) -> str:
        """
        Replace character from the ciphered password with character replacements from the generator configurations
        :param password: The password to perform the action on it
        :return: str: The new ciphered password after character replacements
        """
        translation_table: dict[int, str] = str.maketrans(self.characters_replacements)
        return password.translate(translation_table)

    def generate_password(self, text: str) -> str:
        """
        Generate a strong password string using the raw password (add another layer of encryption to it)
        :param text: The text to generate password from it
        :return: str: The generated ciphered password
        """
        main_algorithm: BaseCipherAlgorithm = self.get_algorithm()
        secondary_algorithm: AffineCipherAlgorithm = AffineCipherAlgorithm(self.shift, self.multiplier)
        intermediate: str = secondary_algorithm.encrypt(f"{self.prefix}{text}{self.postfix}")
        password: str = main_algorithm.encrypt(intermediate)
        password = self.apply_replacements(password)
        return ''.join(c.upper() if c in text else c for c in password)
