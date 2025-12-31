from datetime import datetime, timezone
from fastapi import HTTPException, status, Response, BackgroundTasks
from beanie import PydanticObjectId
from fastapi.responses import JSONResponse

from src.users.schemas import (
    UserRegisterSchema, UserLoginSchema, UserReadSchema,
    UserLoginResponse, UserUpdateSchema, UserAdminRegisterSchema,
    PasswordResetRequestModel, PasswordResetConfirmModel
)
from src.users.models import User
from src.core.security import PWDHashing, BearerTokenClass

from src.utils.url_token import create_url_safe_token, decode_url_safe_token
from src.core.config import Config
from src.utils.mail import send_resend_email_bg


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

    async def password_reset_request(self,
                                     email_data: PasswordResetRequestModel,
                                     bg_tasks: BackgroundTasks):
        email = email_data.email

        token = create_url_safe_token({"email": email})
        frontend_url = f"http://{Config.FRONTEND_DOMAIN}"
        link = f"{frontend_url}/reset-password/{token}"

        subject = "Reset Your Password"
        html_content = f"""
        <h1>Reset Your Password</h1>
        <p>You have requested to reset your password.
        If this was not done by you, kindly ignore this mail</p>
        <p>Please click this <a href="{link}">link</a> to {subject}</p>
        <p>This will expire in 15 minutes.</p>
        <br/>
        <br/>
        <p>PSN AKS</p>
        """

        send_resend_email_bg(bg_tasks,
                             to=email,
                             subject=subject,
                             html=html_content)

        return JSONResponse(
            content={
                "message": "Please check your email for \
    instructions to reset your password",
            },
            status_code=status.HTTP_200_OK,
        )

    async def reset_account_password(self, token: str,
                                     passwords: PasswordResetConfirmModel):
        new_password = passwords.password
        confirm_password = passwords.confirm_password

        if new_password != confirm_password:
            raise HTTPException(
                detail="Passwords do not match",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        token_data = decode_url_safe_token(token)

        user_email = token_data.get("email")

        if user_email:
            user = await self.get_existing_user_by_email(user_email)

            if not user:
                # raise UserNotFound()
                raise HTTPException(
                    detail="User not found",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            passwd_hash = pwd_hashing.generate_password_hash(new_password)

            await user.set({
                "hashed_password": passwd_hash,
                "updated_at": datetime.now(timezone.utc),
            })

            return JSONResponse(
                content={"message": "Password reset Successfully"},
                status_code=status.HTTP_200_OK,
            )

        return JSONResponse(
            content={"message": "Error occured during password reset."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


user_svc = UserService()
