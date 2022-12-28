from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "album" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(25) NOT NULL,
    "description" VARCHAR(500) NOT NULL,
    "poster" VARCHAR(100) NOT NULL,
    "is_hidden" BOOL NOT NULL  DEFAULT False,
    "date_created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_album_name_40d047" ON "album" ("name");;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "album";"""
