from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import Settings
from config.database import setup_database
from src.user.endpoints import router_user

settings = Settings()

app = FastAPI()

setup_database(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_user, prefix='/api/v1', tags=["user"])

