from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "track" ADD "song_poster" VARCHAR(300) NOT NULL;
        ALTER TABLE "track" ALTER COLUMN "song" TYPE VARCHAR(300) USING "song"::VARCHAR(300);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "track" DROP COLUMN "song_poster";
        ALTER TABLE "track" ALTER COLUMN "song" TYPE VARCHAR(100) USING "song"::VARCHAR(100);"""
