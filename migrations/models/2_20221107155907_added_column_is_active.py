from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "is_active" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "user" ALTER COLUMN "password" TYPE VARCHAR(100) USING "password"::VARCHAR(100);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "is_active";
        ALTER TABLE "user" ALTER COLUMN "password" TYPE VARCHAR(50) USING "password"::VARCHAR(50);"""
