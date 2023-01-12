from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(25),
    "last_name" VARCHAR(25),
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(100) NOT NULL,
    "avatar" VARCHAR(1000),
    "date_created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "genre" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(25) NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS "idx_genre_name_c78cd9" ON "genre" ("name");
CREATE TABLE IF NOT EXISTS "album" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(25) NOT NULL,
    "description" VARCHAR(1000) NOT NULL,
    "poster" VARCHAR(1000) NOT NULL,
    "band" VARCHAR(30) NOT NULL,
    "release_year" VARCHAR(10) NOT NULL,
    "is_hidden" BOOL NOT NULL  DEFAULT False,
    "views_count" INT NOT NULL  DEFAULT 0,
    "date_created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_album_name_40d047" ON "album" ("name");
CREATE TABLE IF NOT EXISTS "track" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(30) NOT NULL UNIQUE,
    "track_author" VARCHAR(50) NOT NULL,
    "text" TEXT NOT NULL,
    "date_created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_hidden" BOOL NOT NULL  DEFAULT False,
    "song" VARCHAR(300) NOT NULL,
    "song_poster" VARCHAR(300),
    "views_count" INT NOT NULL  DEFAULT 0,
    "album_id" INT REFERENCES "album" ("id") ON DELETE CASCADE,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_track_name_d54259" ON "track" ("name");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "album_genre" (
    "album_id" INT NOT NULL REFERENCES "album" ("id") ON DELETE CASCADE,
    "genre_id" INT NOT NULL REFERENCES "genre" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "track_genre" (
    "track_id" INT NOT NULL REFERENCES "track" ("id") ON DELETE CASCADE,
    "genre_id" INT NOT NULL REFERENCES "genre" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
