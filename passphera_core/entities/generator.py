from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from cipherspy.cipher import AffineCipherAlgorithm

from passphera_core.entities.generator_config import GeneratorConfig


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
