from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "track" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(30) NOT NULL UNIQUE,
    "track_author" VARCHAR(50) NOT NULL,
    "text" TEXT NOT NULL,
    "date_created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_hidden" BOOL NOT NULL  DEFAULT False,
    "song" VARCHAR(100) NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_track_name_d54259" ON "track" ("name");;
        CREATE TABLE "track_genre" (
    "genre_id" INT NOT NULL REFERENCES "genre" ("id") ON DELETE CASCADE,
    "track_id" INT NOT NULL REFERENCES "track" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "track_genre";
        DROP TABLE IF EXISTS "track";"""
