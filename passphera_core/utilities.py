from cipherspy.cipher import (
    CaesarCipherAlgorithm,
    AffineCipherAlgorithm,
    PlayfairCipherAlgorithm,
    HillCipherAlgorithm)
from passphera_core.exceptions import InvalidPropertyNameException


cipher_registry: dict = {
    'caesar': CaesarCipherAlgorithm,
    'affine': AffineCipherAlgorithm,
    'playfair': PlayfairCipherAlgorithm,
    'hill': HillCipherAlgorithm,
}
default_properties: dict[str, object] = {
    "shift": 3,
    "multiplier": 3,
    "key": "hill",
    "algorithm": "hill",
    "prefix": "secret",
    "postfix": "secret"
}


def check_property_name(func):
    def wrapper(self, prop, *args, **kwargs):
        if prop not in {"shift", "multiplier", "key", "algorithm", "prefix", "postfix", "character_replacements"}:
            raise InvalidPropertyNameException(prop)
        return func(self, prop, *args, **kwargs)
    return wrapper
