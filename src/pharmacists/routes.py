from fastapi import APIRouter, Request, status, Query

from src.pharmacists.schemas import (
    PharmacistReadSchema, PharmacistCreateSchema, PharmacistUpdateSchema
)
# from src.core.dependencies import (
#     RoleChecker, get_current_user, get_token_details
# )
from src.db.session import SessionDep
from src.pharmacists.services import pharmacist_svc


pharmacists_router = APIRouter()
# role_checker = RoleChecker(["admin", "customer"])
# admin_role = RoleChecker(["admin"])


@pharmacists_router.get("", response_model=list[PharmacistReadSchema],
                        status_code=status.HTTP_200_OK)
async def get_pharmacists(request: Request, session: SessionDep,
                          technical_group: str | None = Query(default=None)):
    pharmacists = await pharmacist_svc.get_all_pharmacists(session,
                                                           technical_group)
    return pharmacists


@pharmacists_router.post("", response_model=PharmacistReadSchema,
                         status_code=status.HTTP_201_CREATED)
async def add_pharmacist(request: Request, session: SessionDep,
                         data: PharmacistCreateSchema):
    pharmacist = await pharmacist_svc.add_a_pharmacist(session, data)
    return pharmacist


@pharmacists_router.get("/{license_number}",
                        response_model=PharmacistReadSchema,
                        status_code=status.HTTP_200_OK)
async def get_pharmacist(request: Request, session: SessionDep,
                         license_number: str):
    pharmacist = await pharmacist_svc.get_a_pharmacist(session, license_number)
    return pharmacist


@pharmacists_router.put("/{license_number}",
                        response_model=PharmacistReadSchema,
                        status_code=status.HTTP_200_OK)
async def update_pharmacist(request: Request, session: SessionDep,
                            license_number: str,
                            data: PharmacistUpdateSchema):
    pharmacist = await pharmacist_svc.update_a_pharmacist(session,
                                                          license_number, data)
    return pharmacist


@pharmacists_router.delete("/{license_number}")
async def delete_pharmacist(request: Request, session: SessionDep,
                            license_number: str):
    pharmacist = await pharmacist_svc.delete_a_pharmacist(session,
                                                          license_number)
    return pharmacist


# @pharmacists_router.get("/{uid}", response_model=PharmacistReadSchema,
#                         status_code=status.HTTP_200_OK)
# async def get_pharmacist(request: Request, session: SessionDep,
#                          uid: uuid.UUID):
#     pharmacist = await pharmacist_svc.get_a_pharmacist(session, uid)
#     return pharmacist


# @pharmacists_router.patch("/{uid}", response_model=PharmacistReadSchema,
#                           status_code=status.HTTP_200_OK)
# async def update_pharmacist(request: Request, session: SessionDep,
#                             uid: uuid.UUID,
#                             data: PharmacistUpdateSchema):
#     pharmacist = await pharmacist_svc.update_a_pharmacist(session, uid, data)
#     return pharmacist


# @pharmacists_router.delete("/{uid}")
# async def delete_pharmacist(request: Request, session: SessionDep,
#                             uid: uuid.UUID):
#     pharmacist = await pharmacist_svc.delete_a_pharmacist(session, uid)
#     return pharmacist
