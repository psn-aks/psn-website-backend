from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import DateTime, String
import uuid
from datetime import datetime, timezone


class News(SQLModel, table=True):
    __tablename__ = "news"

    uid: uuid.UUID = Field(primary_key=True, index=True,
                           default_factory=uuid.uuid4)
    title: str = Field(index=True, min_length=2, max_length=150)
    content: Optional[str] = None
    author: str = Field(index=True, min_length=2, max_length=100)
    image_url: str = Field(index=True, min_length=2, max_length=500)
    slug: str = Field(index=True, min_length=2, max_length=180)
    tags: list[str] = Field(default=[], sa_column=Column(ARRAY(String)))
    group: Optional[str] = Field(default="general", index=True,
                                 min_length=2, max_length=50)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=lambda: datetime.now(timezone.utc),
        )
    )

    def __repr__(self):
        return f"<News(Title = {self.title})>"
