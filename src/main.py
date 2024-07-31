from contextlib import asynccontextmanager
from typing import Annotated, Optional, Any

from beanie import init_beanie
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.responses import Response

from db import users_db
from documents import UserDocument
from schemas import RegistrationFormSchema, LoginFormSchema
from security import get_hashed_password, verify_password, issue_jwt, get_jwt_payload, JWTException
from settings import settings


class TokenData(BaseModel):
    token: str


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_beanie(database=users_db, document_models=[UserDocument])
    yield


app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Token = Annotated[str, Depends(oauth2_scheme)]


# Add check that token isn't in blacklist
def get_user_id_from_token(token: Token) -> str:
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials (token expired or blacklisted)",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict[str, Any] = get_jwt_payload(
            token=token,
            key=settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        return payload.get("user_id")
    except JWTException as e:
        raise token_exception from e


UserID = Annotated[str, Depends(get_user_id_from_token)]


@app.post("/register")
async def register(form: RegistrationFormSchema):
    user = UserDocument(
        username=form.username,
        email=form.email,
        password_hash=get_hashed_password(form.password),
    )

    try:
        await UserDocument.insert_one(user)
    except DuplicateKeyError:
        pass

    return Response(status_code=status.HTTP_200_OK)


@app.post("/login")
async def login(form: LoginFormSchema) -> TokenData:
    invalid_credentials_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

    user_by_username: Optional[UserDocument] = await UserDocument.find_one(UserDocument.username == form.login)

    if user_by_username is not None:
        if not verify_password(form.password, user_by_username.password_hash):
            raise invalid_credentials_response

        return TokenData(token=issue_jwt(
            expiration_time_minutes=settings.jwt_expiration_minutes,
            algorithm=settings.jwt_algorithm,
            key=settings.jwt_secret_key,
            user_id=str(user_by_username.id),
        ))

    user_by_email: Optional[UserDocument] = await UserDocument.find_one(UserDocument.email == form.login)
    if user_by_email is not None:
        if not verify_password(form.password, user_by_email.password_hash):
            raise invalid_credentials_response

        return TokenData(token=issue_jwt(
            expiration_time_minutes=settings.jwt_expiration_minutes,
            algorithm=settings.jwt_algorithm,
            key=settings.jwt_secret_key,
            user_id=str(user_by_email.id),
        ))

    raise invalid_credentials_response


@app.post("/logout")
async def logout(user_id: UserID):
    pass


@app.post("/me")
async def me(user_id: UserID) -> Optional[UserDocument]:
    return await UserDocument.get(user_id)
