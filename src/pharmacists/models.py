from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import DateTime, String
import uuid
from datetime import datetime, timezone, date


class PharmacistBase(SQLModel):
    email: Optional[str] = Field(unique=True, index=True, default=None)
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
    interest_groups: list[str] = Field(
        default=[], sa_column=Column(ARRAY(String)))

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
        )
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=lambda: datetime.now(timezone.utc),
        )
    )


class Pharmacist(PharmacistBase, table=True):
    __tablename__ = "pharmacists"

    uid: uuid.UUID = Field(
        index=True,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    def __repr__(self):
        return f"<Pharmacists(fullname = {self.full_name})>"
