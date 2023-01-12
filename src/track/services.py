import boto3

from fastapi import UploadFile

from config.config import Settings

settings = Settings()


async def upload_track_to_s3(file: UploadFile, song_path: str) -> str:
    """ Upload file to s3 bucket """
    s3 = boto3.resource(
        "s3", aws_access_key_id=settings.AWS_BUCKET_KEY_ID, aws_secret_access_key=settings.AWS_BUCKET_SECRET_KEY
    )
    bucket = s3.Bucket(settings.AWS_BUKCET_NAME)
    bucket.upload_fileobj(file.file, song_path, ExtraArgs={"ACL": "public-read"})
    uploaded_file_url = f"https://{settings.AWS_BUKCET_NAME}.s3.amazonaws.com/{song_path}"
    return uploaded_file_url


async def delete_file_to_s3(song_path: str) -> None:
    """ Upload file to s3 bucket """
    s3 = boto3.resource(
        "s3", aws_access_key_id=settings.AWS_BUCKET_KEY_ID, aws_secret_access_key=settings.AWS_BUCKET_SECRET_KEY
    )
    s3.Object(settings.AWS_BUKCET_NAME, song_path[36:]).delete()


async def track_poster_create(user_id: int, song: UploadFile, song_poster: UploadFile) -> tuple[str, str]:
    track_path = 'track/' + f'user_{user_id}/' + song.filename
    track_s3_path = await upload_track_to_s3(song, track_path)
    track_poster_path = 'tracks_posters/' + f'user_{user_id}/' + song_poster.filename
    tracks_poster_s3_path = await upload_track_to_s3(song_poster, track_poster_path)
    return track_s3_path, tracks_poster_s3_path
