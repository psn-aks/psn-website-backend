from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str = "psn_aks"
    JWT_SECRET: str
    JWT_ALGORITHM: str

    REDIS_URL: str = "redis://localhost:6379/0"
    ENVIRONMENT: str = "dev"
    ACCESS_TOKEN_EXPIRY: int = 1800
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    RESEND_API_KEY: str
    MAIL_FROM_RESEND: str
    RESEND_API_URL: str = "https://api.resend.com/emails"

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


Config = Settings()
