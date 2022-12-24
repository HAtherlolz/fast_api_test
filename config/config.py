import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # JWT Setiings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    # Databases settings
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_NAME: str = os.getenv("DB_NAME")

    # SMTP settings
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    EMAILS_FROM_NAME: str = "The IrohWeb and Axizy Band"
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS")
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS")
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS")
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS")

    # Bucket
    AWS_BUCKET_REGION: str = os.getenv("AWS_BUCKET_REGION")
    AWS_BUKCET_NAME: str = os.getenv("AWS_BUKCET_NAME")
    AWS_BUCKET_DEFAULT_AVATAR_PATH: str = f"https://{AWS_BUKCET_NAME}.s3.amazonaws.com/default/UserProfile_small.jpg"
    AWS_BUCKET_KEY_ID: str = os.getenv("AWS_BUCKET_KEY_ID")
    AWS_BUCKET_SECRET_KEY: str = os.getenv("AWS_BUCKET_SECRET_KEY")

    # Allowed Hosts
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",

    ]
