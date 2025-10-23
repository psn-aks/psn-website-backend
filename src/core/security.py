from datetime import datetime, timedelta, timezone
import uuid
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from src.core.config import Config

passwd_context = CryptContext(
    schemes=['bcrypt']
)


DEFAULT_EXPIRY_ACCESS = timedelta(seconds=Config.ACCESS_TOKEN_EXPIRY)
DEFAULT_EXPIRY_REFRESH = timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS)


class PWDHashing:
    def generate_password_hash(self, password: str) -> str:
        hash = passwd_context.hash(password)
        return hash

    def verify_password(self, plain_password: str,
                        hashed_password: str) -> bool:
        return passwd_context.verify(plain_password, hashed_password)


class BearerTokenClass:
    def create_token(self, payload_data: dict,
                     expires_delta: timedelta = None,
                     token_type: str = "access"):
        payload = {}
        payload['sub'] = str(payload_data['user_uid'])
        payload['email'] = payload_data['email']
        payload['role'] = payload_data['role']
        payload['exp'] = datetime.now(timezone.utc) + (
            expires_delta if expires_delta is not None
            else DEFAULT_EXPIRY_ACCESS
        )
        payload['jti'] = str(uuid.uuid4())
        payload['type'] = token_type

        encoded_jwt = jwt.encode(
            payload,
            Config.JWT_SECRET,
            Config.JWT_ALGORITHM
        )

        return encoded_jwt

    def create_access_token(self, data: dict):
        return self.create_token(data, DEFAULT_EXPIRY_ACCESS,
                                 token_type="access")

    def create_refresh_token(self, data: dict):
        return self.create_token(data, DEFAULT_EXPIRY_REFRESH,
                                 token_type="refresh")

    def decode_access_token(self, token: str):
        try:
            payload = jwt.decode(
                token,
                Config.JWT_SECRET,
                algorithms=[Config.JWT_ALGORITHM]
            )
            return (
                payload if payload['exp'] >= datetime.now(
                ).timestamp() else None
            )

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has Expired"
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token"
                )
