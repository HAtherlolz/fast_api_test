from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "first_name" TYPE VARCHAR(225) USING "first_name"::VARCHAR(225);
        ALTER TABLE "user" ALTER COLUMN "last_name" TYPE VARCHAR(225) USING "last_name"::VARCHAR(225);
        ALTER TABLE "genre" ALTER COLUMN "name" TYPE VARCHAR(255) USING "name"::VARCHAR(255);
        ALTER TABLE "album" ALTER COLUMN "name" TYPE VARCHAR(225) USING "name"::VARCHAR(225);
        ALTER TABLE "album" ALTER COLUMN "band" TYPE VARCHAR(255) USING "band"::VARCHAR(255);
        ALTER TABLE "track" ALTER COLUMN "name" TYPE VARCHAR(255) USING "name"::VARCHAR(255);
        ALTER TABLE "track" ALTER COLUMN "song" TYPE VARCHAR(1000) USING "song"::VARCHAR(1000);
        ALTER TABLE "track" ALTER COLUMN "track_author" TYPE VARCHAR(255) USING "track_author"::VARCHAR(255);
        ALTER TABLE "track" ALTER COLUMN "song_poster" TYPE VARCHAR(1000) USING "song_poster"::VARCHAR(1000);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "first_name" TYPE VARCHAR(25) USING "first_name"::VARCHAR(25);
        ALTER TABLE "user" ALTER COLUMN "last_name" TYPE VARCHAR(25) USING "last_name"::VARCHAR(25);
        ALTER TABLE "album" ALTER COLUMN "name" TYPE VARCHAR(25) USING "name"::VARCHAR(25);
        ALTER TABLE "album" ALTER COLUMN "band" TYPE VARCHAR(30) USING "band"::VARCHAR(30);
        ALTER TABLE "genre" ALTER COLUMN "name" TYPE VARCHAR(25) USING "name"::VARCHAR(25);
        ALTER TABLE "track" ALTER COLUMN "name" TYPE VARCHAR(30) USING "name"::VARCHAR(30);
        ALTER TABLE "track" ALTER COLUMN "song" TYPE VARCHAR(300) USING "song"::VARCHAR(300);
        ALTER TABLE "track" ALTER COLUMN "track_author" TYPE VARCHAR(50) USING "track_author"::VARCHAR(50);
        ALTER TABLE "track" ALTER COLUMN "song_poster" TYPE VARCHAR(300) USING "song_poster"::VARCHAR(300);"""
