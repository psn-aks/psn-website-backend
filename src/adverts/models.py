# src/adverts/models.py
from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import String, Boolean, DateTime, Text, Integer
import uuid
from datetime import datetime, timezone


class Advert(SQLModel, table=True):
    __tablename__ = "adverts"

    uid: uuid.UUID = Field(
        primary_key=True,
        index=True,
        default_factory=uuid.uuid4
    )
    title: str = Field(index=True, min_length=2, max_length=255)
    content: Optional[str] = Field(default=None, sa_column=Column(Text()))
    image_url: Optional[str] = Field(
        default=None, sa_column=Column(String(1024)))
    link: Optional[str] = Field(default=None, sa_column=Column(String(1024)))
    start_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True)))
    end_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True)))
    active: bool = Field(
        default=True, sa_column=Column(Boolean(), nullable=False))
    priority: int = Field(default=0, sa_column=Column(
        Integer, nullable=False))  # higher = show first

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
        return f"<Advert(Title = {self.title})>"
