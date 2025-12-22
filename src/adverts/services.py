import uuid
from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException, status

from src.adverts.models import Advert
from src.utils.cloudinary import upload_to_cloudinary


class AdvertsService:

    async def get_all_adverts(
        self,
        offset: int = 0,
        limit: int = 10,
        only_active: bool = False
    ) -> List[Advert]:

        query = Advert.find()

        if only_active:
            now = datetime.now(timezone.utc)

            query = Advert.find(
                {
                    "active": True,
                    "$and": [
                        {
                            "$or": [
                                {"start_date": None},
                                {"start_date": {"$lte": now}},
                            ]
                        },
                        {
                            "$or": [
                                {"end_date": None},
                                {"end_date": {"$gte": now}},
                            ]
                        },
                    ],
                }
            )

        return (
            await query
            .sort([("priority", -1), ("created_at", -1)])
            .skip(offset)
            .limit(limit)
            .to_list()
        )

    async def get_one_advert(
        self,
        advert_uid: uuid.UUID
    ) -> Advert:

        advert = await Advert.find_one(Advert.uid == advert_uid)
        if not advert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Advert not found"
            )
        return advert

    async def create_one_advert(
        self,
        title: str,
        content: str | None,
        link: str | None,
        start_date: datetime | None,
        end_date: datetime | None,
        active: bool = True,
        priority: int = 0,
        image=None,
    ) -> Advert:

        image_url = None
        slug = "adv"  # fix this
        if image:
            image_url = await upload_to_cloudinary(
                image, slug, subfolder="adverts"
            )

        advert = Advert(
            uid=uuid.uuid4(),
            title=title,
            content=content,
            link=link,
            start_date=start_date,
            end_date=end_date,
            active=active,
            priority=priority,
            image_url=image_url,
        )

        await advert.insert()
        return advert

    async def update_one_advert(self, advert_uid, data):
        advert = await Advert.find_one(Advert.uid == advert_uid)
        if not advert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Advert not found",
            )

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(advert, key, value)

        advert.updated_at = datetime.now(timezone.utc)
        await advert.save()
        return advert

    async def delete_one_advert(self, advert_uid):
        advert = await Advert.find_one(Advert.uid == advert_uid)
        if not advert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Advert not found",
            )

        await advert.delete()


adverts_svc = AdvertsService()
