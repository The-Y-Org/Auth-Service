from contextlib import asynccontextmanager
from typing import Annotated

from beanie import init_beanie
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.responses import Response

from db import common
from schemas import RegistrationFormSchema, LoginFormSchema
from security import get_hashed_password
from documents import UserDocument


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_beanie(database=common, document_models=[UserDocument])
    yield


app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Token = Annotated[str, Depends(oauth2_scheme)]


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
async def login(form: LoginFormSchema):
    pass


@app.post("/logout")
async def logout():
    pass


@app.post("/me")
async def me():
    pass
