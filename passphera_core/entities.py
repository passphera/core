import random
from dataclasses import dataclass, field

from cipherspy.cipher import (
    BaseCipherAlgorithm,
    AffineCipherAlgorithm)
from cipherspy.exceptions import InvalidAlgorithmException

from passphera_core.utilities import check_property_name, default_properties, cipher_registry


@dataclass
class Generator:
    shift: int = field(default=default_properties["shift"])
    multiplier: int = field(default=default_properties["multiplier"])
    key: str = field(default=default_properties["key"])
    algorithm: str = field(default=default_properties["algorithm"])
    prefix: str = field(default=default_properties["prefix"])
    postfix: str = field(default=default_properties["postfix"])
    characters_replacements: dict[str, str] = field(default_factory=dict[str, str])

    def get_algorithm(self) -> BaseCipherAlgorithm:
        """
        Get the primary algorithm used to cipher the password
        :return: BaseCipherAlgorithm: The primary algorithm used for the cipher
        """
        algo_name = self.algorithm.lower()
        if algo_name not in cipher_registry:
            raise InvalidAlgorithmException(self.algorithm)
        AlgoClass = cipher_registry[algo_name]
        if algo_name == "caesar":
            return AlgoClass(self.shift)
        elif algo_name == "affine":
            return AlgoClass(self.shift, self.multiplier)
        elif algo_name == "playfair":
            return AlgoClass(self.key)
        elif algo_name == "hill":
            return AlgoClass(self.key)
        raise InvalidAlgorithmException(self.algorithm)

    def get_properties(self) -> dict:
        """
        Retrieves the application properties.

        This method is responsible for providing a dictionary containing
        the current configuration properties of the application. It ensures
        that the properties are properly assembled and returned for use
        elsewhere in the application.

        Returns:
            dict: A dictionary containing the application properties.
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

    @check_property_name
    def get_property(self, prop: str):
        """
        Get the value of a specific generator property
        :param prop: The property name to retrieve; must be one of: shift, multiplier, key, algorithm, prefix, postfix
        :raises InvalidPropertyNameException: If the property name is not one of the allowed properties
        :return: The value of the requested property
        """
        return getattr(self, prop)

    @check_property_name
    def set_property(self, prop: str, value: str):
        """
        Update a generator property with a new value
        :param prop: The property name to update; must be one of: shift, multiplier, key, algorithm, prefix, postfix
        :param value: The new value to set for the property
        :raises ValueError: If the property name is not one of the allowed properties
        :return: None
        """
        if prop in ["shift", "multiplier"]:
            value = int(value)
        setattr(self, prop, value)
        if prop == "algorithm":
            self.get_algorithm()

    @check_property_name
    def reset_property(self, prop: str) -> None:
        """
        Reset a generator property to its default value
        :param prop: The property name to reset, it must be one of: shift, multiplier, key, algorithm, prefix, postfix
        :raises ValueError: If the property name is not one of the allowed properties
        :return: None
        """
        setattr(self, prop, default_properties[prop])
        if prop == "algorithm":
            self.get_algorithm()

    def get_character_replacement(self, character: str) -> str:
        """
        Get the replacement string for a given character
        :param character: The character to get its replacement
        :return: str: The replacement string for the character, or the character itself if no replacement exists
        """
        return self.characters_replacements.get(character, character)

    def set_character_replacement(self, character: str, replacement: str) -> None:
        """
        Replace a character with another character or set of characters
        Eg: pg.replace_character('a', '@1')
        :param character: The character to be replaced
        :param replacement: The (character|set of characters) to replace the first one
        :return: None
        """
        self.characters_replacements[character[0]] = replacement

    def reset_character_replacement(self, character: str) -> None:
        """
        Reset a character to its original value (remove its replacement from characters_replacements)
        :param character: The character to be reset to its original value
        :return: None
        """
        self.characters_replacements.pop(character, None)

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
        for char, repl in self.characters_replacements.items():
            password = password.replace(char, repl)
        password_chars = list(password)
        alpha_indices = [i for i, char in enumerate(password_chars) if char.isalpha()]
        if alpha_indices:
            num_to_upper = max(1, len(alpha_indices) // 2)
            indices_to_upper = random.sample(alpha_indices, num_to_upper)
            for i in indices_to_upper:
                password_chars[i] = password_chars[i].upper()
        return "".join(password_chars)
