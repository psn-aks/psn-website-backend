import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import (
    APIRouter, HTTPException, status, UploadFile,
    Request, Query, Form, File
    )

from src.db.session import SessionDep
from .models import Advert
from .schemas import AdvertRead, AdvertUpdate
from .services import adverts_svc


adverts_router = APIRouter()


@adverts_router.get("/", response_model=List[AdvertRead])
async def list_adverts(
    request: Request,
    session: SessionDep,
    only_active: bool = Query(
        False, description="Return only currently active adverts"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):

    adverts_list = await adverts_svc.get_all_adverts(session, offset,
                                                     limit, only_active)
    return adverts_list


@adverts_router.get("/{advert_uid}", response_model=AdvertRead)
async def get_advert(request: Request, session: SessionDep,
                     advert_uid: uuid.UUID):

    advert = await adverts_svc.get_one_advert(session, advert_uid)
    return advert


@adverts_router.post("/", response_model=AdvertRead,
                     status_code=status.HTTP_201_CREATED)
async def create_advert(
        request: Request,
        session: SessionDep,
        title: str = Form(...),
        content: Optional[str] = Form(None),
        link: Optional[str] = Form(None),
        start_date: Optional[datetime] = Form(None),
        end_date: Optional[datetime] = Form(None),
        active: Optional[bool] = Form(True),
        priority: Optional[int] = Form(0),
        image: Optional[UploadFile] = File(None)):

    advert = await adverts_svc.create_one_advert(session, title, content,
                                                 link, start_date, end_date,
                                                 active, priority, image)
    return advert


@adverts_router.put("/{advert_uid}", response_model=AdvertRead)
async def update_advert(
        request: Request,
        advert_uid: int,
        ad_update: AdvertUpdate,
        session: SessionDep):
    advert = await session.get(Advert, advert_uid)
    if not advert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Advert not found")

    update_data = ad_update.dict(exclude_unset=True)
    for key, val in update_data.items():
        setattr(advert, key, val)
    advert.updated_at = datetime.utcnow()
    session.add(advert)
    await session.commit()
    await session.refresh(advert)
    return advert


@adverts_router.delete("/{advert_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_advert(advert_uid: uuid.UUID, session: SessionDep):
    advert = await session.get(Advert, advert_uid)
    if not advert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Advert not found")
    await session.delete(advert)
    await session.commit()
    return None
