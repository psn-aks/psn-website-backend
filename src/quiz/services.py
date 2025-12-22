from fastapi import HTTPException, status

from src.quiz.models import QuizTopic
from src.quiz.schemas import QuizTopicCreate, QuizTopicRead
from src.utils.slugify import generate_slug_from_title


class QuizService:
    async def list_topics(self):
        quiz_topics = await QuizTopic.find_all().to_list()

        return [await QuizTopicRead.from_mongo(q) for q in quiz_topics]

    async def create_topic(self, topic: QuizTopicCreate):

        slug = await generate_slug_from_title(topic.title, QuizTopic)

        quiz_topic = QuizTopic(
            title=topic.title,
            description=topic.description,
            slug=slug
        )

        await quiz_topic.insert()
        return await QuizTopicRead.from_mongo(quiz_topic)

    async def get_topic(self, slug: str):
        quiz_topic = await QuizTopic.find_one(QuizTopic.slug == slug)
        if not quiz_topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Topic not found"
            )
        return await QuizTopicRead.from_mongo(quiz_topic)


quiz_svc = QuizService()
