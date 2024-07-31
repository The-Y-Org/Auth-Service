from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.responses import Response

from db import user_collection
from schemas import RegistrationFormSchema, LoginFormSchema, UserSchema
from security import get_hashed_password


@asynccontextmanager
async def lifespan(app_: FastAPI):
    user_collection.create_index("email", unique=True)
    user_collection.create_index("username", unique=True)
    yield


app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Token = Annotated[str, Depends(oauth2_scheme)]


@app.post("/register")
async def register(form: RegistrationFormSchema):
    user = UserSchema(
        username=form.username,
        email=form.email,
        password_hash=get_hashed_password(form.password),
    )

    try:
        await user_collection.insert_one(user.model_dump(exclude={"id"}))
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
