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

    def get_settings(self) -> dict:
        """
        Retrieves the application settings.

        This method is responsible for providing a dictionary containing
        the current configuration settings of the application. It ensures
        that the settings are properly assembled and returned for use
        elsewhere in the application.

        Returns:
            dict: A dictionary containing the application settings.
        """
        return {
            "shift": self.shift,
            "multiplier": self.multiplier,
            "key": self.key,
            "algorithm": self.algorithm,
            "prefix": self.prefix,
            "postfix": self.postfix,
            "characters_replacements": self.characters_replacements,
        }

    def set_property(self, property: str, value: str):
        """
        Update a generator property with a new value
        :param property: The property name to update; must be one of: shift, multiplier, key, algorithm, prefix, postfix
        :param value: The new value to set for the property
        :raises ValueError: If the property name is not one of the allowed properties
        :return: None
        """
        if property not in {"shift", "multiplier", "key", "algorithm", "prefix", "postfix"}:
            raise ValueError(f"Invalid property: {property}")
        if property in ["shift", "multiplier"]:
            value = int(value)
        setattr(self, property, value)
        if property == "algorithm":
            self.get_algorithm()
        self.updated_at = datetime.now(timezone.utc)
        
    def reset_property(self, property: str):
        """
        Reset a generator property to its default value
        :param property: The property name to reset, it must be one of: shift, multiplier, key, algorithm, prefix, postfix
        :raises ValueError: If the property name is not one of the allowed properties
        :return: None
        """
        if property not in {"shift", "multiplier", "key", "algorithm", "prefix", "postfix"}:
            raise ValueError(f"Invalid property: {property}")

        defaults = {
            "shift": 3,
            "multiplier": 3,
            "key": "hill",
            "algorithm": "hill",
            "prefix": "secret",
            "postfix": "secret"
        }

        setattr(self, property, defaults[property])
        if property == "algorithm":
            self.get_algorithm()
        self.updated_at = datetime.now(timezone.utc)

    def replace_character(self, char: str, replacement: str) -> None:
        """
        Replace a character with another character or set of characters
        Eg: pg.replace_character('a', '@1')
        :param char: The character to be replaced
        :param replacement: The (character|set of characters) to replace the first one
        :return: None
        """
        self.characters_replacements[char[0]] = replacement
        self.updated_at = datetime.now(timezone.utc)

    def reset_character(self, char: str) -> None:
        """
        Reset a character to its original value (remove its replacement from characters_replacements)
        :param char: The character to be reset to its original value
        :return: None
        """
        self.characters_replacements.pop(char, None)
        self.updated_at = datetime.now(timezone.utc)

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
        password = password.translate(str.maketrans(self.characters_replacements))
        return ''.join(c.upper() if c in text else c for c in password)
