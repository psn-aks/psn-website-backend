import uuid
from fastapi import APIRouter, Request, status, UploadFile, File, Form, Query

from src.news.schemas import NewsDetailResponse, NewsRead, NewsUpdate

# from src.core.dependencies import (
#     RoleChecker, get_current_user, get_token_details
# )
from src.db.session import SessionDep
from src.news.services import news_svc

news_router = APIRouter()
# role_checker = RoleChecker(["admin", "customer"])
# admin_role = RoleChecker(["admin"])


@news_router.get("", response_model=list[NewsRead],
                 status_code=status.HTTP_200_OK)
async def list_news(request: Request, session: SessionDep,
                    group: str | None = Query(default=None)):
    news_list = await news_svc.get_all_news(session, group)
    return news_list


@news_router.post("", response_model=NewsRead,
                  status_code=status.HTTP_201_CREATED)
async def add_news(request: Request,
                   session: SessionDep,
                   title: str = Form(...),
                   author: str = Form(...),
                   content: str = Form(...),
                   tags: str = Form(None),
                   group: str = Form(None),
                   image: UploadFile = File(None)
                   ):
    tag_list = tags.split(",") if tags else []
    news = await news_svc.add_a_news(session, title, author, content,
                                     tag_list, group, image)
    return news


@news_router.get("/{uid}", response_model=NewsRead,
                 status_code=status.HTTP_200_OK)
async def get_news(request: Request, session: SessionDep,
                   uid: uuid.UUID):
    news = await news_svc.get_a_news(session, uid)
    return news


@news_router.put("/{uid}", response_model=NewsRead,
                 status_code=status.HTTP_200_OK)
async def update_news(request: Request, session: SessionDep,
                      uid: uuid.UUID,
                      data: NewsUpdate):
    news = await news_svc.update_a_news(session, uid, data)
    return news


@news_router.delete("/{uid}")
async def delete_news(request: Request, session: SessionDep,
                      uid: uuid.UUID):
    news = await news_svc.delete_a_news(session, uid)
    return news


@news_router.get("/slug/{slug}", response_model=NewsDetailResponse,
                 status_code=status.HTTP_200_OK)
async def get_news_by_slug(request: Request, session: SessionDep,
                           slug: str):
    news = await news_svc.get_a_news_by_slug(session, slug)
    return news


@news_router.put("/slug/{slug}", response_model=NewsRead,
                 status_code=status.HTTP_200_OK)
async def update_news_by_slug(request: Request,
                              session: SessionDep,
                              slug: str,
                              title: str = Form(None),
                              author: str = Form(None),
                              content: str = Form(None),
                              tags: str = Form(None),
                              group: str = Form(None),
                              image: UploadFile = File(None)):
    tag_list = tags.split(",") if tags else None
    news = await news_svc.update_a_news_by_slug(session=session,
                                                slug=slug,
                                                title=title,
                                                author=author,
                                                content=content,
                                                tags=tag_list,
                                                group=group,
                                                image=image)
    return news


@news_router.delete("/slug/{slug}")
async def delete_news_by_slug(request: Request, session: SessionDep,
                              slug: str):
    news = await news_svc.delete_a_news_by_slug(session, slug)
    return news
