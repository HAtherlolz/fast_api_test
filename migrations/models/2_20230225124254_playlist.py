from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "playlist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "description" VARCHAR(1000) NOT NULL,
    "is_hidden" BOOL NOT NULL  DEFAULT False,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_playlist_name_66d68d" ON "playlist" ("name");
COMMENT ON TABLE "playlist" IS 'Model for playlists ';;
        CREATE TABLE "playlist_track" (
    "track_id" INT NOT NULL REFERENCES "track" ("id") ON DELETE CASCADE,
    "playlist_id" INT NOT NULL REFERENCES "playlist" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "playlist_track";
        DROP TABLE IF EXISTS "playlist";"""
