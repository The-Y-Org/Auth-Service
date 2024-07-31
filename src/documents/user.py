from datetime import datetime

from beanie import Document, Indexed
from pydantic import Field


class UserDocument(Document):
    username: Indexed(str, unique=True)
    email: Indexed(str, unique=True)
    password_hash: str
    creation_date: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
