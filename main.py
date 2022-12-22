from fastapi import FastAPI
from config.database import setup_database
from src.user.endpoints import router_user

app = FastAPI()

setup_database(app)

app.include_router(router_user, prefix='/api/v1', tags=["user"])

