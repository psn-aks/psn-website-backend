import uuid
from datetime import datetime, timezone
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from src.adverts.models import Advert
from src.utils.image_upload import upload_image
# from src.adverts.schemas import


class AdvertsService:
    async def get_all_adverts(self, session: AsyncSession, offset: int,
                              limit: int, only_active: bool):

        stmt = select(Advert).order_by(Advert.priority.desc(),
                                       Advert.created_at.desc()).offset(
                                           offset
        ).limit(limit)

        if only_active:
            now = datetime.now(timezone.utc)
            # active flag true, start_date <= now (or null),
            # end_date >= now (or null)
            stmt = stmt.where(
                Advert.active.is_(True),
                (Advert.start_date.is_(None)) | (Advert.start_date <= now),
                (Advert.end_date.is_(None)) | (Advert.end_date >= now),
            )

        result = await session.exec(stmt)
        return result.all()

    async def get_one_advert(self, session: AsyncSession,
                             advert_uid: uuid.UUID):
        advert = await session.get(Advert, advert_uid)
        if not advert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Advert not found")
        return advert

    async def create_one_advert(self, session: AsyncSession,
                                title, content,
                                link, start_date, end_date,
                                active, priority, image):

        advert = Advert(
            title=title,
            content=content,
            link=link,
            start_date=start_date,
            end_date=end_date,
            active=active,
            priority=priority,
            image_url=await upload_image(image)
        )

        session.add(advert)
        await session.commit()
        await session.refresh(advert)
        return advert


adverts_svc = AdvertsService()
