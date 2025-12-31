import logging
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from src.core.config import Config


serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET,
    salt="email-configuration"
)


def create_url_safe_token(data: dict):
    token = serializer.dumps(data)
    return token


def decode_url_safe_token(token: str, max_age: int = 900):
    try:
        token_data = serializer.loads(token, max_age=max_age)
        return token_data
    except SignatureExpired:
        logging.warning("Token has expired")
        return None
    except BadSignature:
        logging.warning("Invalid token")
        return None
