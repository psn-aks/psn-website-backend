from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from bson import ObjectId


class UserMiniResponse(BaseModel):
    id: str
    email: EmailStr
    fullname: str
    is_admin: bool


class UserMiniSchema(BaseModel):
    id: str
    email: EmailStr
    fullname: str
    is_admin: bool

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(max_length=40)
    fullname: str
    password: str = Field(min_length=6)


class UserAdminRegisterSchema(UserRegisterSchema):
    is_admin: bool = False


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserMiniResponse


class UserReadSchema(BaseModel):
    id: str = Field(alias="_id", json_schema_extra={
        "example": "652c1e6fcf9b7f001f3f5a2b"
    })
    email: EmailStr
    fullname: str
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    @classmethod
    async def from_mongo(cls, user):
        if isinstance(user, dict):
            data = user.copy()
        else:
            data = user.model_dump(by_alias=True)

        if "_id" in data:
            data['_id'] = str(data['_id'])

        return cls(**data)


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    fullname: Optional[str] = None
    is_admin: Optional[bool] = None
