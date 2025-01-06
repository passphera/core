class InvalidAlgorithmException(Exception):
    def __init__(self, algorithm: str) -> None:
        super().__init__(f"Invalid algorithm name [{algorithm}]")
