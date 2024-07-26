from fastapi import FastAPI

from schemas import RegistrationFormSchema, LoginFormSchema

app = FastAPI()


@app.get("/")
async def register(form: RegistrationFormSchema):
    pass


async def login(form: LoginFormSchema):
    pass


async def logout():
    pass


async def me():
    pass
