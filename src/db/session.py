from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
import psycopg
# from psycopg.ex

from src.core.config import Config


def ensure_database_exists():
    url = urlparse(Config.DATABASE_URL.replace("+asyncpg", ""))

    dbname = url.path.lstrip("/")
    user = url.username
    password = url.password
    host = url.hostname or "localhost"
    port = url.port or 5432

    conn = psycopg.connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host,
        port=port
    )

    conn.autocommit = True

    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}';")
    exists = cur.fetchone()

    if not exists:
        cur.execute(f'CREATE DATABASE "{dbname}";')
        print(f"Database '{dbname}' created.")
    else:
        print(f"Database '{dbname}' already exists.")
    cur.close()
    conn.close()


ensure_database_exists()


engine = create_async_engine(Config.DATABASE_URL, future=True)


async def init_db():
    if Config.ENVIRONMENT == "dev":
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            print("Database connected and tables ready (dev mode)")


async def get_session():
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
