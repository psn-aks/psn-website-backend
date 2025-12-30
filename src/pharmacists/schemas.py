from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId


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
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None


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
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None


class PharmacistReadSchema(PharmacistBaseSchema):
    id: str = Field(alias="_id", json_schema_extra={
        "example": "652c1e6fcf9b7f001f3f5a2b"
    })

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    @classmethod
    async def from_mongo(cls, pharmacist):
        if isinstance(pharmacist, dict):
            data = pharmacist.copy()
        else:
            data = pharmacist.model_dump(by_alias=True)

        if "_id" in data:
            data['_id'] = str(data['_id'])

        return cls(**data)
