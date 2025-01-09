from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from cryptography.fernet import Fernet

from cipherspy.cipher import *
from cipherspy.cipher.base_cipher import BaseCipherAlgorithm
from cipherspy.utilities import generate_salt, derive_key

from passphera_core import exceptions


@dataclass
class Password:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default=datetime.now(timezone.utc))
    updated_at: datetime = field(default=datetime.now(timezone.utc))
    context: str = field(default_factory=str)
    text: str = field(default_factory=str)
    password: str = field(default_factory=str)
    salt: bytes = field(default_factory=bytes)

    def encrypt(self) -> None:
        self.salt = generate_salt()
        key = derive_key(self.password, self.salt)
        self.password = Fernet(key).encrypt(self.password.encode()).decode()

    def decrypt(self) -> str:
        key = derive_key(self.password, self.salt)
        return Fernet(key).decrypt(self.password.encode()).decode()


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
            raise exceptions.InvalidAlgorithmException(self.algorithm)
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


@dataclass
class Generator:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    config: GeneratorConfig = field(default_factory=GeneratorConfig)

    def apply_replacements(self, password: str) -> str:
        """
        Replace character from the ciphered password with character replacements from the generator configurations
        :return: str: The new ciphered password after character replacements
        """
        translation_table = str.maketrans(self.config.characters_replacements)
        return password.translate(translation_table)

    def generate_password(self, text: str) -> str:
        """
        Generate a strong password string using the raw password (add another layer of encryption to it)
        :return: str: The generated ciphered password
        """
        affine = AffineCipherAlgorithm(self.config.shift, self.config.multiplier)
        intermediate = affine.encrypt(f"{self.config.prefix}{text}{self.config.postfix}")
        main_algorithm = self.config.get_algorithm()
        password = main_algorithm.encrypt(intermediate)
        password = self.apply_replacements(password)
        return ''.join(c.upper() if c in text else c for c in password)


@dataclass
class User:
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    username: str = field(default_factory=str)
    email: str = field(default_factory=str)
    password: str = field(default_factory=str)
    generator: UUID = field(default_factory=UUID)
    passwords: list[UUID] = field(default_factory=list[UUID])

    def add_password(self, password_id: UUID) -> None:
        self.passwords.append(password_id)

    def delete_password(self, password_id: UUID) -> None:
        self.passwords.remove(password_id)
