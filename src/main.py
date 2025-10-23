import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.middlewares import register_middleware
from src.middlewares.rate_limit import apply_rate_limit_to_router

from src.pharmacists.routes import pharmacists_router
from src.news.routes import news_router
from src.adverts.routes import adverts_router
from src.contact.routes import contact_router

base_prefix = "/api/v1"


app = FastAPI(
    title="PSN AKS API",
    openapi_url=f"{base_prefix}/openapi.json",
    docs_url=f"{base_prefix}/docs",
    redoc_url=f"{base_prefix}/redoc",
)


register_middleware(app)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount(f"/{UPLOAD_DIR}", StaticFiles(directory=UPLOAD_DIR), name=UPLOAD_DIR)


@app.get(f"{base_prefix}/")
def home():
    return "Welcome to the PSN AKS API"


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
