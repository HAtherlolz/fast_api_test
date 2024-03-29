from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.config import Settings
from config.database import setup_database

from src.user.endpoints import router_user
from src.genre.endpoints import genre_router
from src.track.endpoints import track_router
from src.album.endpoints import album_router
from src.playlist.endpoints import playlist_router

settings = Settings()

app = FastAPI(
    openapi_url="/api/v1/",
    docs_url="/api/v1/docs/",
    redoc_url="/api/v1/redoc/",
    title="IrohAxi",
    description="Authors - IrohWeb and Axizy",
    version="1.0.1",
)

setup_database(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_user, prefix='/api/v1', tags=["user"])
app.include_router(genre_router, prefix='/api/v1', tags=["genre"])
app.include_router(track_router, prefix='/api/v1', tags=["track"])
app.include_router(album_router, prefix='/api/v1', tags=["album"])
app.include_router(playlist_router, prefix='/api/v1', tags=["playlist"])

