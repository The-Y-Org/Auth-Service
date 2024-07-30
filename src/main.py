from fastapi import FastAPI

from schemas import RegistrationFormSchema, LoginFormSchema

app = FastAPI()


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
