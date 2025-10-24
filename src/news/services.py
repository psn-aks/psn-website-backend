import os
from typing import Optional
import uuid
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_
from sqlalchemy import func
from fastapi import File, HTTPException, UploadFile, status

from src.news.models import News
from src.news.schemas import NewsUpdate
from src.utils.image_upload import upload_image
from src.utils.slug import slugify

# from src.core.security import BearerTokenClass, PWDHashing
# from src.db.redis import add_jti_to_blocklist

# pwd_hashing = PWDHashing()
# jwt_bearer_token = BearerTokenClass()


class NewsService:

    async def get_news_by_uid(self, session: AsyncSession,
                              uid: uuid.UUID):
        news = await session.get(News, uid)
        if not news:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News not found")
        return news

    async def get_news_by_slug(self, session: AsyncSession,
                               slug: str):
        query = select(News).where(News.slug == slug)
        result = await session.exec(query)
        news = result.first()
        if not news:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News not found")
        return news

    async def get_all_news(self, session: AsyncSession,
                           group: Optional[str] = None):

        query = select(News).order_by(News.created_at.desc())

        if group:
            group_list = [g.strip().lower()
                          for g in group.split(",") if g.strip()]
            if group_list:
                filters = [News.group.ilike(f"%{g}%") for g in group_list]
                query = query.where(or_(*filters))

        result = await session.exec(query)
        news_list = result.all()
        return news_list

    async def add_a_news(self, session: AsyncSession,
                         title: str,
                         author: str,
                         content: str,
                         tags: list[str] = [],
                         group: str = None,
                         image: UploadFile = File(None)
                         ):

        slug_title = slugify(title)
        slug_datetime = slugify(str(datetime.now(timezone.utc)))
        slug = f"{slug_title}-{slug_datetime}"

        news = News(
            title=title,
            author=author,
            content=content,
            tags=tags,
            slug=slug,
            group=group,
            image_url=await upload_image(image, subfolder="news")
        )

        session.add(news)
        await session.commit()
        await session.refresh(news)
        return news

    async def get_a_news(self, session: AsyncSession,
                         uid: uuid.UUID):
        news = await self.get_news_by_uid(session, uid)
        return news

    async def update_a_news(self, session: AsyncSession,
                            uid: uuid.UUID,
                            data: NewsUpdate):
        news = await self.get_news_by_uid(session, uid)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(news, key, value)

        session.add(news)
        await session.commit()
        await session.refresh(news)
        return news

    async def delete_a_news(self, session: AsyncSession, uid: uuid.UUID):

        news = await self.get_news_by_uid(session, uid)

        await session.delete(news)
        await session.commit()
        return JSONResponse(
            content="News deleted successfully",
            status_code=status.HTTP_200_OK
        )

    async def get_related_news(
        self,
        session: AsyncSession,
        tags: list[str],
        current_slug: str,
        limit: int = 3
    ):
        """Fetch related news articles sharing similar tags."""
        if not tags:
            return []

        stmt = (
            select(News)
            .where(
                func.array_length(News.tags, 1).isnot(None),
                News.slug != current_slug
            )
            .order_by(News.created_at.desc())
            .limit(limit)
        )

        result = await session.exec(stmt)
        related_news = result.all()
        return related_news

    async def get_a_news_by_slug(self,
                                 session: AsyncSession,
                                 slug: str):
        news = await self.get_news_by_slug(session, slug)
        related = await self.get_related_news(session, news.tags,
                                              news.slug)
        return {
            "article": news,
            "related": related,
        }

    async def update_a_news_by_slug(self, session: AsyncSession,
                                    slug: str,
                                    title: str | None = None,
                                    author: str | None = None,
                                    content: str | None = None,
                                    tags: list[str] | None = None,
                                    group: list[str] | None = None,
                                    image: UploadFile | None = None
                                    ):
        news = await self.get_news_by_slug(session, slug)

        if title:
            news.title = title
            date = datetime.now(timezone.utc)
            news.slug = f"{slugify(title)}-{slugify(str(date))}"
        if author:
            news.author = author
        if content:
            news.content = content
        if tags is not None:
            news.tags = tags
        if group is not None:
            news.group = group

        if image:
            if news.image and os.path.exists(news.image):
                os.remove(news.image)
            image_url = await upload_image(image, subfolder="news")
            news.image = image_url

        news.updated_at = datetime.now(timezone.utc)

        session.add(news)
        await session.commit()
        await session.refresh(news)
        return news

    async def delete_a_news_by_slug(self, session: AsyncSession, slug: str):

        news = await self.get_news_by_slug(session, slug)

        await session.delete(news)
        await session.commit()
        return JSONResponse(
            content="News deleted successfully",
            status_code=status.HTTP_200_OK
        )


news_svc = NewsService()
