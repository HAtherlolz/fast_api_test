from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise


def get_db_uri(*, user, password, host, db):
    return f'postgres://{user}:{password}@{host}:5432/{db}'


def setup_database(app: FastAPI):
    register_tortoise(
        app,
        db_url=get_db_uri(
            user='postgres',
            password='1003kv2000',
            host='localhost',
            db='fastapi',
        ),
        modules={
            'models': [
                'models',
                "aerich.models"
            ],
        },
        generate_schemas=True,
        add_exception_handlers=True,
    )


TORTOISE_ORM = {
    "connections": {"default": get_db_uri(
            user='postgres',
            password='1003kv2000',
            host='localhost',
            db='fastapi',
        )},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


Tortoise.init_models(["models"], "models")
