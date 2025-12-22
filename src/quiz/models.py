from datetime import datetime, timezone
from beanie import Document, PydanticObjectId
from pydantic import Field


class QuizTopic(Document):
    title: str
    description: str | None = None
    slug: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "quiz_topics"
        indexes = [
            "title",
        ]


class QuizQuestion(Document):
    topic_id: PydanticObjectId
    topic_slug: str
    question: str
    options: list[str]  # exactly 4 options
    correct_index: int  # 0-3
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "quiz_questions"
        indexes = [
            "topic_id",
            "topic_slug"
        ]
