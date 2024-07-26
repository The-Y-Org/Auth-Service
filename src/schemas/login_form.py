from typing import Optional

from pydantic import BaseModel


class LoginFormSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str
