from pydantic import BaseModel


class LoginFormSchema(BaseModel):
    login: str  # username of email
    password: str
