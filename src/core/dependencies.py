from typing import Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

from src.auth.models import User
from src.core.security import BearerTokenClass
from src.db.redis import token_in_blocklist
from src.db.session import SessionDep
from src.auth.services import user_svc

oauth2_dep = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

jwt_bearer_token = BearerTokenClass()


def get_token_details(token: str = Depends(oauth2_dep)):
    token_details = jwt_bearer_token.decode_access_token(token)
    return token_details


def refresh_token_details(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    token = auth_header.split(" ")[1]
    token_details = get_token_details(token)
    if token_details.get('type') != 'refresh':
        raise HTTPException(
            detail="Please provide a valid refresh token",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return token_details


async def get_current_user(session: SessionDep,
                           token: str = Depends(oauth2_dep)):
    token_details = get_token_details(token)
    if await token_in_blocklist(token_details['jti']):
        raise HTTPException(
            detail="Token has been revoked. Please log in again.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    user_email = token_details['email']

    user = await user_svc.get_user_by_email(user_email, session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: list[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(
            detail="Access forbidden. Insufficient Permission",
            status_code=status.HTTP_403_FORBIDDEN
        )
