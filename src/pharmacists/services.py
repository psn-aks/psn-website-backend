from typing import Optional
import uuid
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from src.pharmacists.models import Pharmacist
from src.pharmacists.schemas import (
    PharmacistCreateSchema, PharmacistUpdateSchema
)

# from src.core.security import BearerTokenClass, PWDHashing
# from src.db.redis import add_jti_to_blocklist

# pwd_hashing = PWDHashing()
# jwt_bearer_token = BearerTokenClass()


class PharmacistService:

    async def get_pharmacist_by_uid(self, session: AsyncSession,
                                    uid: uuid.UUID):
        pharmacist = await session.get(Pharmacist, uid)
        if not pharmacist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pharmacist not found")
        return pharmacist

    async def get_pharmacist_by_license_number(self, session: AsyncSession,
                                               license_number: str):
        query = select(Pharmacist).where(
            Pharmacist.pcn_license_number == license_number
        )
        result = await session.exec(query)
        pharmacist = result.first()
        if not pharmacist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pharmacist not found")
        return pharmacist

    async def get_all_pharmacists(self, session: AsyncSession,
                                  technical_group: Optional[str] = None):

        if technical_group:
            query = select(Pharmacist).where(
                Pharmacist.technical_group == technical_group
            )
        else:
            query = select(Pharmacist)

        result = await session.exec(query)
        pharmacists = result.all()
        return pharmacists

    async def add_a_pharmacist(self, session: AsyncSession,
                               data: PharmacistCreateSchema):
        pharmacist = Pharmacist(**data.model_dump())

        session.add(pharmacist)
        await session.commit()
        await session.refresh(pharmacist)
        return pharmacist

    async def get_a_pharmacist(self, session: AsyncSession,
                               license_number: str):
        # pharmacist = await self.get_pharmacist_by_uid(session, uid)
        pharmacist = await self.get_pharmacist_by_license_number(
            session, license_number)
        return pharmacist

    async def update_a_pharmacist(self, session: AsyncSession,
                                  license_number: str,
                                  data: PharmacistUpdateSchema):
        pharmacist = await self.get_pharmacist_by_license_number(
            session, license_number)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(pharmacist, key, value)

        session.add(pharmacist)
        await session.commit()
        await session.refresh(pharmacist)
        return pharmacist

    async def delete_a_pharmacist(self, session: AsyncSession,
                                  license_number: str):

        pharmacist = await self.get_pharmacist_by_license_number(
            session, license_number)
        await session.delete(pharmacist)
        await session.commit()

        return JSONResponse(
            content="Pharmacist deleted successfully",
            status_code=status.HTTP_200_OK
        )


pharmacist_svc = PharmacistService()
