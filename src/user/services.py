from datetime import timedelta

import boto3

from fastapi import UploadFile
from pathlib import Path

from config.config import Settings
from .serializers import User_Pydantic
from .jwt_auth import create_access_token
from ..utils.email import send_email

settings = Settings()


def send_test_email(email_to: str, token: str):
    """
        send activation email
    """
    project_name = settings.EMAILS_FROM_NAME
    subject = f"{project_name} - Test email"
    with open(Path(__file__).parent.parent / 'email_templates' / "registration.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"protocol": "http", "domain": "localhost:8080", "url": token},
    )


async def upload_file_to_s3(file: UploadFile, image_path: str) -> str:
    """ Upload file to s3 bucket """
    s3 = boto3.resource(
        "s3", aws_access_key_id=settings.AWS_BUCKET_KEY_ID, aws_secret_access_key=settings.AWS_BUCKET_SECRET_KEY
    )
    bucket = s3.Bucket(settings.AWS_BUKCET_NAME)
    bucket.upload_fileobj(file.file, image_path, ExtraArgs={"ACL": "public-read"})
    uploaded_file_url = f"https://{settings.AWS_BUKCET_NAME}.s3.amazonaws.com/{image_path}"
    return uploaded_file_url


async def delete_file_to_s3(image_path: str) -> None:
    """ Upload file to s3 bucket """
    s3 = boto3.resource(
        "s3", aws_access_key_id=settings.AWS_BUCKET_KEY_ID, aws_secret_access_key=settings.AWS_BUCKET_SECRET_KEY
    )
    s3.Object(settings.AWS_BUKCET_NAME, image_path[36:]).delete()


async def get_jwt(user: User_Pydantic) -> str:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 24 * 7)
    user_info = {
        "sub": user.email,
        "user_id": user.id
    }
    access_token = create_access_token(
        data=user_info, expires_delta=access_token_expires
    )
    return access_token
