from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from schemas import RegistrationFormSchema, LoginFormSchema

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Token = Annotated[str, Depends(oauth2_scheme)]


@app.get("/")
async def register(form: RegistrationFormSchema):
    pass


@app.post("/login")
async def login(form: LoginFormSchema):
    pass


@app.post("/logout")
async def logout():
    pass


@app.post("/me")
async def me():
    pass
