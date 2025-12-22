from fastapi import APIRouter, Request

health_router = APIRouter()


@health_router.get("/")
async def health(request: Request,):
    return {"status": "ok"}


@health_router.get("/debug/cookies")
def debug_cookies(request: Request):
    return request.cookies
