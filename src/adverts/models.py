from typing import Optional
from beanie import Document, Indexed, before_event
from beanie.odm.actions import Update
from pydantic import Field
from datetime import datetime, timezone
import uuid
from typing_extensions import Annotated


class Advert(Document):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4)

    title: Annotated[str, Indexed()] = Field(
        min_length=2,
        max_length=255
    )

    content: Optional[str] = None
    image_url: Optional[str] = Field(max_length=1024)
    link: Optional[str] = Field(max_length=1024)

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    active: bool = Field(default=True)
    priority: int = Field(default=0)  # higher = show first

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "adverts"
        indexes = [
            "title",
            "active",
            "priority",
            "start_date",
            "end_date",
        ]

    def __repr__(self):
        return f"<Advert title={self.title}>"

    @before_event(Update)
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)
