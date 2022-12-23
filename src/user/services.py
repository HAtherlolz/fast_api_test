import base64
import boto3

from fastapi import UploadFile
from pathlib import Path
from pydantic import BaseModel, EmailStr
# from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from config.config import Settings
from .serializers import User_Pydantic

settings = Settings()


# conf = ConnectionConfig(
#     MAIL_USERNAME=settings.MAIL_USERNAME,
#     MAIL_PASSWORD=settings.MAIL_PASSWORD,
#     MAIL_FROM=settings.MAIL_FROM,
#     MAIL_PORT=settings.MAIL_PORT,
#     MAIL_SERVER=settings.MAIL_SERVER,
#     MAIL_STARTTLS=settings.MAIL_STARTTLS,
#     MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
#     USE_CREDENTIALS=settings.USE_CREDENTIALS,
#     VALIDATE_CERTS=settings.VALIDATE_CERTS,
#     TEMPLATE_FOLDER=Path(__file__).parent.parent / 'email_templates'
# )
#
#
# class EmailSchema(BaseModel):
#     email: list[EmailStr]
#
#
# html = """
#     <p>Thanks for using Fastapi-mail</p>
# """
#
#
# async def send_with_template(email: EmailSchema, uuid: str):
#     user_dict = {
#         "protocol": 'http',
#         "domain": "127.0.0.1:8000",
#         "url": f"uuid={uuid}"
#     }
#
#     message = MessageSchema(
#         subject="Fastapi-Mail module",
#         recipients=[email],
#         template_body=user_dict,
#         subtype=MessageType.html,
#         )
#
#     fm = FastMail(conf)
#     await fm.send_message(message, template_name="registration.html")


# async def send_email(email: EmailSchema) -> None:
#     """ Email sending """
#     message = MessageSchema(
#         subject="Fastapi-Mail module",
#         recipients=[email],
#         body=html,
#         subtype=MessageType.html
#     )
#     fm = FastMail(conf)
#     await fm.send_message(message)


async def encode_uuid(id: str) -> str:
    encoded_id = id.encode('ascii')
    base64_bytes = base64.urlsafe_b64encode(encoded_id).rstrip(b'\n=').decode('ascii')
    return base64_bytes


async def decode_uuid(uuid: str) -> int:
    uuid = uuid.encode('ascii')
    return int(base64.urlsafe_b64decode(uuid.ljust(len(uuid) + len(uuid) % 4, b'=')))


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
