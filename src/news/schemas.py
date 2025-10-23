import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


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
    uid: uuid.UUID
    created_at: datetime
    slug: str
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NewsDetailResponse(BaseModel):
    article: NewsRead
    related: list[NewsRead] = []

    class Config:
        from_attributes = True
