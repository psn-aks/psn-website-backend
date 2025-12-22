from typing import List
from fastapi import (
    APIRouter, HTTPException, status, Request, Depends, Response
)

from src.core.dependencies import require_admin
from src.users.schemas import (
    UserRegisterSchema, UserLoginSchema, UserReadSchema, UserLoginResponse,
    UserUpdateSchema, UserAdminRegisterSchema
)
from src.users.services import user_svc
from src.users.models import User

user_router = APIRouter()


@user_router.post("/auth/register", response_model=UserReadSchema,
                  status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, user_data: UserRegisterSchema):
    return await user_svc.register_user(user_data)


# add dependency here
@user_router.post("/auth/admin/register", response_model=UserReadSchema,
                  status_code=status.HTTP_201_CREATED)
async def admin_register_user(request: Request,
                              user_data: UserAdminRegisterSchema,
                              current_admin: User = Depends(require_admin)):
    return await user_svc.admin_register_user(user_data)


@user_router.post("/auth/login", response_model=UserLoginResponse,
                  status_code=status.HTTP_200_OK)
async def login_user(request: Request, user_data: UserLoginSchema,
                     response: Response):
    return await user_svc.login_user(user_data, response)


# @user_router.get("/{email}", response_model=UserReadSchema,
#                  status_code=status.HTTP_200_OK)
# async def get_user(request: Request, email: str):
#     return await user_svc.get_user(email)


@user_router.get("", response_model=List[UserReadSchema],
                 status_code=status.HTTP_200_OK)
async def get_users(request: Request):
    return await user_svc.get_users()


@user_router.get("/{user_id}", response_model=UserReadSchema,
                 status_code=status.HTTP_200_OK)
async def get_user_by_id(request: Request, user_id: str):
    return await user_svc.get_user_by_id(user_id)


@user_router.put("/{user_id}", response_model=UserReadSchema,
                 status_code=status.HTTP_200_OK)
async def update_user_by_id(request: Request, user_id: str,
                            user_data: UserUpdateSchema):
    return await user_svc.update_user_by_id(user_id, user_data)


@user_router.delete("/{user_id}",
                    status_code=status.HTTP_200_OK)
async def delete_user_by_id(request: Request, user_id: str):
    return await user_svc.delete_user_by_id(user_id)


@user_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/"
    )
    return {"detail": "Logged out successfully"}


@user_router.post("/auth/refresh",
                  status_code=status.HTTP_200_OK)
async def refresh_access_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )
    return await user_svc.refresh_access_token(refresh_token, response)
