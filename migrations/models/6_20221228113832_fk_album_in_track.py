from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "album" ALTER COLUMN "poster" TYPE VARCHAR(300) USING "poster"::VARCHAR(300);
        ALTER TABLE "track" ADD "album_id" INT;
        ALTER TABLE "track" ADD CONSTRAINT "fk_track_album_1a4c3472" FOREIGN KEY ("album_id") REFERENCES "album" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "track" DROP CONSTRAINT "fk_track_album_1a4c3472";
        ALTER TABLE "album" ALTER COLUMN "poster" TYPE VARCHAR(100) USING "poster"::VARCHAR(100);
        ALTER TABLE "track" DROP COLUMN "album_id";"""
