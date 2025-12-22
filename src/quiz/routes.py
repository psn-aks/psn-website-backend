from typing import List
from fastapi import APIRouter, HTTPException
from src.quiz.models import QuizTopic, QuizQuestion
from src.quiz.schemas import QuizQuestionUpdate, QuizTopicCreate, QuizTopicRead
from src.quiz.services import quiz_svc
from bson import ObjectId

quiz_router = APIRouter()


@quiz_router.get("/topics", response_model=List[QuizTopicRead])
async def list_topics():
    return await quiz_svc.list_topics()


@quiz_router.post("/topics", response_model=QuizTopic)
async def create_topic(topic: QuizTopicCreate):
    return await quiz_svc.create_topic(topic)


@quiz_router.get("/topics/{topic_id}", response_model=QuizTopic)
async def get_topic_id(topic_id: str):
    db_topic = await QuizTopic.get(topic_id)
    if not db_topic:
        raise HTTPException(404, "Topic not found")
    return db_topic


@quiz_router.put("/topics/{topic_id}", response_model=QuizTopic)
async def update_topic(topic_id: str, topic: QuizTopic):
    db_topic = await QuizTopic.get(topic_id)
    if not db_topic:
        raise HTTPException(404, "Topic not found")
    await db_topic.update({"$set": topic.dict(exclude_unset=True)})
    return db_topic


@quiz_router.delete("/topics/{topic_id}")
async def delete_topic(topic_id: str):
    db_topic = await QuizTopic.get(topic_id)
    if not db_topic:
        raise HTTPException(404, "Topic not found")
    await db_topic.delete()
    return {"detail": "Deleted"}


@quiz_router.get("/topics/slug/{slug}", response_model=QuizTopicRead)
async def get_topic(slug: str):
    return await quiz_svc.get_topic(slug)


# --- Questions ---


@quiz_router.get("/topics/{topic_id}/questions",
                 response_model=List[QuizQuestion])
async def list_questions(topic_id: str):
    print(topic_id)
    return await QuizQuestion.find({"topic_id": ObjectId(topic_id)}).to_list()


@quiz_router.get("/topics/slug/{slug}/questions",
                 response_model=List[QuizQuestion])
async def list_questions_slug(slug: str):
    print(slug)
    return await QuizQuestion.find({"topic_slug": slug}).to_list()


@quiz_router.post("/questions", response_model=QuizQuestion)
async def create_question(question: QuizQuestion):
    await question.insert()
    return question


@quiz_router.put("/questions/{question_id}", response_model=QuizQuestion)
async def update_question(question_id: str, question: QuizQuestionUpdate):

    db_q = await QuizQuestion.get(question_id)
    if not db_q:
        raise HTTPException(404, "Question not found")
    await db_q.update({"$set": question.dict(exclude_unset=True)})
    return db_q


@quiz_router.delete("/questions/{question_id}")
async def delete_question(question_id: str):
    db_q = await QuizQuestion.get(question_id)
    if not db_q:
        raise HTTPException(404, "Question not found")
    await db_q.delete()
    return {"detail": "Deleted"}
