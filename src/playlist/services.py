import boto3

from fastapi import UploadFile

from config.config import Settings

settings = Settings()


async def upload_playlist_poster_to_s3(file: UploadFile, poster_path: str) -> str:
    """ Upload file to s3 bucket """
    s3 = boto3.resource(
        "s3", aws_access_key_id=settings.AWS_BUCKET_KEY_ID, aws_secret_access_key=settings.AWS_BUCKET_SECRET_KEY
    )
    bucket = s3.Bucket(settings.AWS_BUKCET_NAME)
    bucket.upload_fileobj(file.file, poster_path, ExtraArgs={"ACL": "public-read"})
    uploaded_file_url = f"https://{settings.AWS_BUKCET_NAME}.s3.amazonaws.com/{poster_path}"
    return uploaded_file_url

async def delete_file_to_s3(play_list_path: str) -> None:
    """ Upload file to s3 bucket """
    s3 = boto3.resource(
        "s3", aws_access_key_id=settings.AWS_BUCKET_KEY_ID, aws_secret_access_key=settings.AWS_BUCKET_SECRET_KEY
    )
    s3.Object(settings.AWS_BUKCET_NAME, play_list_path[36:]).delete()