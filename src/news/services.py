from typing import Optional, List, Tuple
from datetime import datetime, timezone
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from src.news.models import News
from src.news.schemas import NewsRead
from src.utils.cloudinary import upload_to_cloudinary
from src.utils.slugify import generate_slug_from_title


class NewsService:

    async def get_news(self, slug: str) -> News:
        news = await News.find_one(News.slug == slug)
        if not news:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News not found"
            )
        return news

    async def get_news_by_slug(self, slug: str) -> NewsRead:
        news = await self.get_news(slug)
        return await NewsRead.from_mongo(news)

    async def get_all_news(
        self,
        page: int = 1,
        limit: int = 5,
        q: Optional[str] = None,
        group: Optional[str] = None,
    ) -> Tuple[list[NewsRead], int]:

        skip = (page - 1) * limit

        filters = {}

        if group:
            group_list = [g.strip().lower()
                          for g in group.split(",") if g.strip()]
            if group_list:
                filters["group"] = {"$in": group_list}

        if q:
            filters["$or"] = [
                {"title": {"$regex": q, "$options": "i"}},
                {"content": {"$regex": q, "$options": "i"}},
                {"author": {"$regex": q, "$options": "i"}},
            ]

        query = News.find(filters).sort(-News.created_at)

        total = await query.count()

        results = await query.skip(skip).limit(limit).to_list()

        items = [await NewsRead.from_mongo(n) for n in results]

        return items, total

    async def add_a_news(
        self,
        title: str,
        author: str,
        content: str,
        tags: List[str] | None = None,
        group: Optional[str] = None,
        image: UploadFile | None = None
    ) -> News:

        tags = tags or []

        slug = await generate_slug_from_title(title, News)

        image_url = await upload_to_cloudinary(image, slug,
                                               subfolder="news")

        news = News(
            title=title,
            author=author,
            content=content,
            tags=tags,
            slug=slug,
            group=group,
            image_url=image_url,
        )

        await news.insert()
        return await NewsRead.from_mongo(news)

    # async def update_a_news(
    #     self,
    #     uid: uuid.UUID,
    #     data: NewsUpdate
    # ) -> News:

    #     news = await self.get_news_by_uid(uid)

    #     update_data = data.model_dump(exclude_unset=True)
    #     for key, value in update_data.items():
    #         setattr(news, key, value)

    #     news.updated_at = datetime.now(timezone.utc)
    #     await news.save()
    #     return news

    # async def delete_a_news(self, uid: uuid.UUID):

    #     news = await self.get_news_by_uid(uid)
    #     await news.delete()

    #     return JSONResponse(
    #         content="News deleted successfully",
    #         status_code=status.HTTP_200_OK
    #     )

    async def get_related_news(
        self,
        tags: List[str],
        current_slug: str,
        limit: int = 3
    ) -> List[News]:

        if not tags:
            return []

        related_news = await News.find(
            {
                "tags": {"$in": tags},
                "slug": {"$ne": current_slug},
            }
        ).sort(-News.created_at).limit(limit).to_list()

        return [await NewsRead.from_mongo(n) for n in related_news]

    async def get_a_news_by_slug(self, slug: str):
        news = await self.get_news_by_slug(slug)
        related = await self.get_related_news(news.tags, news.slug)

        return {
            "article": news,
            "related": related,
        }

    async def update_a_news_by_slug(
        self,
        slug: str,
        title: str | None = None,
        author: str | None = None,
        content: str | None = None,
        tags: List[str] | None = None,
        group: Optional[str] = None,
        image: UploadFile | None = None
    ) -> News:

        news = await self.get_news(slug)

        if title:
            news.title = title
            news.slug = await generate_slug_from_title(title, News)

        if author:
            news.author = author
        if content:
            news.content = content
        if tags is not None:
            news.tags = tags
        if group is not None:
            news.group = group

        if image:
            news.image_url = await upload_to_cloudinary(
                image, slug, subfolder="news")

        news.updated_at = datetime.now(timezone.utc)
        await news.save()

        return await NewsRead.from_mongo(news)

    async def delete_a_news_by_slug(self, slug: str):

        news = await self.get_news(slug)
        await news.delete()

        return JSONResponse(
            content="News deleted successfully",
            status_code=status.HTTP_200_OK
        )


news_svc = NewsService()
