from typing import Optional, Annotated, List
from beanie import Document, Indexed, before_event
from beanie.odm.actions import Update
from datetime import datetime, timezone
from pydantic import Field


class News(Document):

    title: str = Field(index=True, min_length=2, max_length=150)
    content: Optional[str] = None
    author: str = Field(index=True, min_length=2, max_length=100)
    image_url: str = Field(index=True, min_length=2, max_length=500)
    slug: str = Annotated[str, Indexed(unique=True)]
    tags: List[str] = Field(default_factory=list)
    group: Optional[str] = Field(default="general",
                                 min_length=2, max_length=50)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @before_event(Update)
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)

    class Settings:
        name = "news"
        indexes = [
            "title",
            "author",
            "image_url",
            "group",
        ]
