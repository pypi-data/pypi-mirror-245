from typing import Optional


class SecretValue:
    pass


class AWSSecretsManagerValue(SecretValue):
    def __init__(self, name: str, path: Optional[str] = None) -> None:
        ...


class AWSParameterStoreValue(SecretValue):
    def __init__(self, name: str, path: Optional[str] = None) -> None:
        ...
