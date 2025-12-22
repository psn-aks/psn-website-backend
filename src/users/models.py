from typing import Annotated
from beanie import Document, Indexed
from pydantic import Field, EmailStr
from typing import Optional
from datetime import datetime, timezone


class User(Document):

    email: Annotated[EmailStr, Indexed(unique=True)]
    fullname: Optional[str]
    password_hash: str
    is_admin: bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    deleted_at: Optional[datetime] = None

    class Settings:
        name = "users"
