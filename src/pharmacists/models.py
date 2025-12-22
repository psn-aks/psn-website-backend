from typing import Annotated
from beanie import Document, Indexed
from pydantic import Field, EmailStr
from typing import Optional
from datetime import datetime, timezone, date


class Pharmacist(Document):
    email: Annotated[EmailStr, Indexed(unique=True)]
    full_name: str
    fellow: Optional[str] = None
    school_attended: Optional[str] = None
    pcn_license_number: str
    induction_year: int
    date_of_birth: Optional[date] = None
    residential_address: Optional[str] = None
    place_of_work: Optional[str] = None
    technical_group: str
    gender: str
    phone_number: str
    interest_groups: list[str] = []
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "pharmacists"
