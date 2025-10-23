import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, ValidationInfo


class AdvertBase(BaseModel):
    title: str
    content: Optional[str] = None
    image_url: Optional[str] = None
    link: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    active: Optional[bool] = True
    priority: Optional[int] = 0

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v, info: ValidationInfo):
        start = info.data.get("start_date")
        if v is not None and start is not None and v < start:
            raise ValueError("end_date must be after start_date")
        return v


class AdvertCreate(AdvertBase):
    pass


class AdvertUpdate(AdvertBase):
    title: Optional[str] = None


class AdvertRead(AdvertBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
