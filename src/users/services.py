from datetime import datetime, timezone
from fastapi import HTTPException, status, Response
from beanie import PydanticObjectId

from src.users.schemas import (
    UserRegisterSchema, UserLoginSchema, UserReadSchema,
    UserLoginResponse, UserUpdateSchema, UserAdminRegisterSchema
)
from src.users.models import User
from src.core.security import PWDHashing, BearerTokenClass


pwd_hashing = PWDHashing()
jwt_bearer_token = BearerTokenClass()


class UserService:

    async def get_existing_user_by_email(self, email):
        user = await User.find_one(User.email == email)
        return user

    async def register_user(self, user_data: UserRegisterSchema):
        if await self.get_existing_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email Address already registered"
            )

        user_data_dict = user_data.model_dump()

        user_data_dict["password_hash"] = \
            pwd_hashing.generate_password_hash(
                user_data.password
        )

        user = User(**user_data_dict)
        await user.insert()
        return await UserReadSchema.from_mongo(user)

    async def admin_register_user(self, user_data: UserAdminRegisterSchema):
        if await self.get_existing_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email Address already registered"
            )

        user_data_dict = user_data.model_dump()

        user_data_dict["password_hash"] = \
            pwd_hashing.generate_password_hash(
                user_data.password
        )

        user = User(**user_data_dict)
        await user.insert()
        return await UserReadSchema.from_mongo(user)

    async def login_user(self, user_data: UserLoginSchema, response: Response):
        user = await self.get_existing_user_by_email(user_data.email)
        if not user:
            raise HTTPException(
                detail="Invalid Username or Password",
                status_code=status.HTTP_403_FORBIDDEN
            )

        if not pwd_hashing.verify_password(user_data.password,
                                           user.password_hash):
            raise HTTPException(
                detail="Invalid Username or Password",
                status_code=status.HTTP_403_FORBIDDEN
            )

        payload = {
            "email": user.email,
            "user_id": str(user.id),
            "is_admin": user.is_admin
        }

        access_token = jwt_bearer_token.create_access_token(payload)
        refresh_token = jwt_bearer_token.create_refresh_token(payload)
        user_res = {
            "email": user.email,
            "id": str(user.id),
            "is_admin": user.is_admin,
            "fullname": user.fullname

        }
        print(access_token)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,           # use False for local development
            samesite="none",
            path="/"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,           # use False for local development
            samesite="none",
            path="/"
        )

        return UserLoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user_res
        )

    async def get_user(self, email: str):
        user = await self.get_existing_user_by_email(email)

        return await UserReadSchema.from_mongo(user)

    async def get_users(self):
        filters = {
            "deleted_at": None,
        }
        users = await User.find(filters).to_list()

        return [await UserReadSchema.from_mongo(user) for user in users]

    async def get_user_by_id(self, user_id: str):
        user = await User.get(PydanticObjectId(user_id))
        print(user_id)
        print(user)
        if not user:
            raise HTTPException(
                detail="User not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        return await UserReadSchema.from_mongo(user)

    async def delete_user_by_id(self, user_id: str):
        user = await User.get(PydanticObjectId(user_id))
        if not user:
            raise HTTPException(
                detail="User not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        user.deleted_at = datetime.now(timezone.utc)

        await user.save()

        return {"message": "User deleted"}

    async def update_user_by_id(self, user_id: str,
                                user_data: UserUpdateSchema):
        user = await User.get(PydanticObjectId(user_id))
        if not user:
            raise HTTPException(
                detail="User not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        user_data_dict = user_data.model_dump(exclude_unset=True)
        user_data_dict["updated_at"] = datetime.now(timezone.utc)

        await user.set(user_data_dict)

        return await UserReadSchema.from_mongo(user)

    async def refresh_access_token(self, refresh_token: str,
                                   response: Response):

        payload = jwt_bearer_token.decode_token(
            refresh_token, token_type="refresh")

        user_id = payload.get("sub")
        user = await User.get(PydanticObjectId(user_id))

        if not user or user.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )

        new_payload = {
            "email": user.email,
            "user_id": str(user.id),
            "is_admin": user.is_admin
        }

        access_token = jwt_bearer_token.create_access_token(new_payload)
        refresh_token = jwt_bearer_token.create_refresh_token(new_payload)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="none",
            path="/"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="none",
            path="/"
        )

        return {"message": "Access token refreshed"}


user_svc = UserService()
