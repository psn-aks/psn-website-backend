
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.core.config import Config


async def init_db(app: FastAPI):

    from src.pharmacists.models import Pharmacist
    from src.adverts.models import Advert
    from src.news.models import News
    from src.users.models import User
    from src.quiz.models import QuizTopic, QuizQuestion

    mongo_uri = Config.MONGO_URI
    db_client = AsyncIOMotorClient(mongo_uri)
    db = db_client[Config.DB_NAME]

    docs = [Pharmacist, Advert, News, User, QuizTopic, QuizQuestion]

    await init_beanie(database=db, document_models=docs)

    app.state.mongo_client = db_client
