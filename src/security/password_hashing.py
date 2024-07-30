from passlib.context import CryptContext


class InvalidHashException(Exception):
    def __init__(self, message: str, hash_: str):
        super().__init__(message)
        self.__hash = hash_

    @property
    def hash(self):
        return self.__hash


pwd_context = CryptContext(
    schemes=['argon2']
)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(secret=password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(secret=plain_password, hash=hashed_password)
    except ValueError as e:
        raise InvalidHashException(message='verifying password failed', hash_=hashed_password) from e
