from datetime import datetime, date
from typing import List, Optional
import uuid
from pydantic import BaseModel, Field


class PharmacistBaseSchema(BaseModel):
    email: Optional[str] = None
    full_name: str
    fellow: Optional[str] = None
    school_attended: Optional[str] = None
    pcn_license_number: str
    induction_year: int
    date_of_birth: Optional[date] = None
    residential_address: Optional[str] = None
    place_of_work: Optional[str] = None
    technical_group: str
    interest_groups: List[str] = Field(default_factory=list)
    gender: str


# class PharmacistReadSchema(BaseModel):
#     uid: uuid.UUID
#     email: Optional[str] = None
#     full_name: str
#     fellow: Optional[str] = None
#     school_attended: Optional[str] = None
#     pcn_license_number: str
#     induction_year: int
#     date_of_birth: Optional[date] = None
#     residential_address: Optional[str] = None
#     place_of_work: Optional[str] = None
#     technical_group: str
#     interest_groups: list[str]
#     created_at: datetime
#     updated_at: datetime


class PharmacistCreateSchema(PharmacistBaseSchema):
    pass


class PharmacistUpdateSchema(BaseModel):

    email: Optional[str] = None
    full_name: Optional[str] = None
    fellow: Optional[str] = None
    school_attended: Optional[str] = None
    pcn_license_number: Optional[str] = None
    induction_year: Optional[int] = None
    date_of_birth: Optional[date] = None
    residential_address: Optional[str] = None
    place_of_work: Optional[str] = None
    technical_group: Optional[str] = None
    interest_groups: Optional[List[str]] = None
    gender: Optional[str] = None


class PharmacistReadSchema(PharmacistBaseSchema):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
