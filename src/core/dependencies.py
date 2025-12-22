from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.users.models import User
from src.core.security import BearerTokenClass
# from src.db.redis import token_in_blocklist
from src.users.services import user_svc


jwt_bearer_token = BearerTokenClass()

bearer_scheme = HTTPBearer(auto_error=False)


def get_token_details(request: Request,
                      credentials: HTTPAuthorizationCredentials = Depends(
                          bearer_scheme)
                      ) -> dict:

    token = request.cookies.get("access_token")
    print("token in cookies: ", token)
    if not token and credentials:
        token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing"
        )

    token_details = jwt_bearer_token.decode_token(token, token_type="access")
    if not token_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid"
        )
    return token_details

# def refresh_token_details(request: Request):
#     auth_header = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Bearer "):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Missing or invalid Authorization header"
#         )
#     token = auth_header.split(" ")[1]
#     token_details = get_token_details(token)
#     if token_details.get('type') != 'refresh':
#         raise HTTPException(
#             detail="Please provide a valid refresh token",
#             status_code=status.HTTP_401_UNAUTHORIZED
#         )
#     return token_details


async def get_current_user(token_details: dict = Depends(get_token_details)):
    # if await token_in_blocklist(token_details['jti']):
    #     raise HTTPException(
    #         detail="Token has been revoked. Please log in again.",
    #         status_code=status.HTTP_401_UNAUTHORIZED
    #     )
    user_email = token_details['email']
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = await user_svc.get_existing_user_by_email(user_email)
    print(user)
    return user


# class RoleChecker:
#     def __init__(self, allowed_roles: list[str]) -> None:
#         self.allowed_roles = allowed_roles

#     def __call__(self, current_user: User = Depends(
    # get_current_user)) -> Any:
#         if current_user.role in self.allowed_roles:
#             return True
#         raise HTTPException(
#             detail="Access forbidden. Insufficient Permission",
#             status_code=status.HTTP_403_FORBIDDEN
#         )


async def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
