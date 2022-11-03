from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "city" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL UNIQUE,
    "file" VARCHAR(2000),
    "timezone" DATE NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(50) NOT NULL,
    "date_created" DATE NOT NULL,
    "date_updated" DATE NOT NULL,
    "city_id" INT REFERENCES "city" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
