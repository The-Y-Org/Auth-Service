from datetime import datetime, timedelta
from typing import Any

import jwt


class JWTException(Exception):
    def __init__(self, message: str, token: str) -> None:
        super().__init__(message)
        self.__token = token

    @property
    def token(self) -> str:
        return self.__token


class JWTExpiredException(JWTException):
    pass


class JWTInvalidSignatureException(JWTException):
    pass


def issue_jwt(expiration_time_minutes: int, algorithm: str, key: str, **kwargs) -> str:
    return jwt.encode(
        payload={
            "exp": datetime.utcnow() + timedelta(minutes=expiration_time_minutes),
            **kwargs
        },
        key=key,
        algorithm=algorithm,
    )


def get_jwt_payload(token: str, key: str, algorithms: list[str]) -> dict[str, Any]:
    common_message: str = "getting payload failed"

    try:
        return jwt.decode(jwt=token, key=key, algorithms=algorithms)
    except jwt.ExpiredSignatureError as e:
        raise JWTExpiredException(message=common_message, token=token) from e
    except jwt.InvalidTokenError as e:
        raise JWTInvalidSignatureException(message=common_message, token=token) from e
