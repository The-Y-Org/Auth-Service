from typing import Annotated, Optional

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.responses import Response

from db import user_collection
from schemas import RegistrationFormSchema, LoginFormSchema, UserSchema
from security import get_hashed_password

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Token = Annotated[str, Depends(oauth2_scheme)]


@app.post("/register")
async def register(form: RegistrationFormSchema):
    success_response = Response(status_code=status.HTTP_200_OK)

    found_by_username: Optional[dict] = await user_collection.find_one({
        "username": form.username
    })
    if found_by_username is not None:
        return success_response

    found_by_email: Optional[dict] = await user_collection.find_one({
        "email": form.email
    })
    if found_by_email is not None:
        return success_response

    user = UserSchema(
        username=form.username,
        email=form.email,
        password_hash=get_hashed_password(form.password),
    )

    await user_collection.insert_one(user.model_dump(exclude={"id"}))

    return success_response


@app.post("/login")
async def login(form: LoginFormSchema):
    pass


@app.post("/logout")
async def logout():
    pass


@app.post("/me")
async def me():
    pass
