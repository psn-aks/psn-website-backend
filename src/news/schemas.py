from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId


class NewsBase(BaseModel):
    title: str
    content: str
    tags: Optional[list[str]] = None
    author: Optional[str] = None
    image_url: Optional[str] = None
    group: Optional[str] = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    slug: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[list[str]] = None
    group: Optional[str] = None


class NewsRead(NewsBase):
    id: str = Field(alias="_id", json_schema_extra={
        "example": "652c1e6fcf9b7f001f3f5a2b"
    })
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    @classmethod
    async def from_mongo(cls, news):
        if isinstance(news, dict):
            data = news.copy()
        else:
            data = news.model_dump(by_alias=True)

        if "_id" in data:
            data['_id'] = str(data['_id'])

        return cls(**data)


class NewsDetailResponse(BaseModel):
    article: NewsRead
    related: list[NewsRead] = []

    class Config:
        from_attributes = True
