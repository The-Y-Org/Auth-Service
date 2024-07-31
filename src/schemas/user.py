from datetime import datetime
from typing import Optional, Annotated

from pydantic import BaseModel, Field, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserSchema(BaseModel):
    id: Optional[PyObjectId] = Field(validation_alias="_id", default=None)
    username: str
    email: str
    password_hash: str
    creation_date: datetime = Field(default_factory=datetime.utcnow)
