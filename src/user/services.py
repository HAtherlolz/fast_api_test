from datetime import timedelta

import boto3

from fastapi import UploadFile
from pathlib import Path

from config.config import Settings
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
        environment={"protocol": "https", "domain": "irohaxi.site", "url": token},
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

