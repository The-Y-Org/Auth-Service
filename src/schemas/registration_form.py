from pydantic import BaseModel


class RegistrationFormSchema(BaseModel):
    username: str
    email: str
    password: str
