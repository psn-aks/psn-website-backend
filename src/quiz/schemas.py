from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from beanie import PydanticObjectId
from bson import ObjectId


class QuizTopicBase(BaseModel):
    title: str
    description: Optional[str] = None


class QuizTopicCreate(QuizTopicBase):
    pass


class QuizTopicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class QuizTopicRead(QuizTopicBase):
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
    async def from_mongo(cls, quiz_topic):
        if isinstance(quiz_topic, dict):
            data = quiz_topic.copy()
        else:
            data = quiz_topic.model_dump(by_alias=True)

        if "_id" in data:
            data['_id'] = str(data['_id'])

        return cls(**data)


class QuizQuestionUpdate(BaseModel):
    topic_id: Optional[PydanticObjectId] = None
    topic_slug: Optional[str] = None
    question: Optional[str] = None
    options: Optional[list[str]] = None
    correct_index: Optional[int] = None
