from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
import urllib.parse

from .config import Settings

settings = Settings()


def get_db_uri(*, user, password, host, db):
    password = urllib.parse.quote_plus(password)
    return f'postgres://{user}:{password}@{host}:5432/{db}'


def setup_database(app: FastAPI):
    print(settings.DB_USER)
    register_tortoise(
        app,
        db_url=get_db_uri(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            db=settings.DB_NAME,
        ),
        modules={
            'models': [
                'src.unit.models',
                'src.user.models',
                "aerich.models"
            ],
        },
        generate_schemas=True,
        add_exception_handlers=True,
    )


TORTOISE_ORM = {
    "connections": {"default": get_db_uri(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            db=settings.DB_NAME,
        )},
    "apps": {
        "models": {
            "models": ['src.unit.models', "src.user.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


Tortoise.init_models(["models"], "models")
