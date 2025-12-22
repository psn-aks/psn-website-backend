from fastapi import FastAPI
from contextlib import asynccontextmanager
from mangum import Mangum


from src.db.connection import init_db

from src.middlewares import register_middleware
# from src.middlewares.rate_limit import apply_rate_limit_to_router

from src.users.routes import user_router
from src.pharmacists.routes import pharmacists_router
from src.news.routes import news_router
from src.adverts.routes import adverts_router
from src.contact.routes import contact_router
from src.quiz.routes import quiz_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting...")
    client = await init_db(app)
    try:
        yield
    finally:
        print("Server has stopped!!!")
        if client:
            client.close()

base_prefix = "/api/v1"


def register_routers(app: FastAPI) -> None:

    # apply_rate_limit_to_router(pharmacists_router, "30/minute")
    app.include_router(
        user_router, prefix=f"{base_prefix}/users",
        tags=["users"]
    )

    # apply_rate_limit_to_router(pharmacists_router, "30/minute")
    app.include_router(
        pharmacists_router, prefix=f"{base_prefix}/pharmacists",
        tags=["pharmacists"]
    )

    # apply_rate_limit_to_router(news_router, "30/minute")
    app.include_router(
        news_router, prefix=f"{base_prefix}/news", tags=["news"]
    )

    # apply_rate_limit_to_router(news_router, "30/minute")
    app.include_router(
        adverts_router, prefix=f"{base_prefix}/adverts", tags=["adverts"]
    )

    # apply_rate_limit_to_router(news_router, "30/minute")
    app.include_router(
        contact_router, prefix=f"{base_prefix}/contact", tags=["contact"]
    )

    # apply_rate_limit_to_router(news_router, "30/minute")
    app.include_router(
        quiz_router, prefix=f"{base_prefix}/quiz", tags=["quiz"]
    )


def create_app() -> FastAPI:

    app = FastAPI(
        title="PSN AKS API",
        openapi_url=f"{base_prefix}/openapi.json",
        docs_url=f"{base_prefix}/docs",
        redoc_url=f"{base_prefix}/redoc",
        lifespan=life_span
    )

    @app.get(f"{base_prefix}/")
    def home():
        return "Welcome to the PSN AKS API"

    register_middleware(app)
    register_routers(app)

    return app


app = create_app()

handler = Mangum(app)
