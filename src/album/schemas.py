from typing import Union, List
from datetime import datetime

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.user.serializers import User_Pydantic
from src.track.schema import Track_Pydantic, Genre
from .models import Album


List_Album = pydantic_model_creator(Album, name="AlbumList", exclude=('track', 'genre'))
Album_Pydantic = pydantic_model_creator(Album, name='Album')
# AlbumUpdate = pydantic_model_creator(Album, name='AlbumUpdate', exclude=("owner", ))
AlbumIn_Pydantic = pydantic_model_creator(Album, name='AlbumIn', exclude_readonly=True, exclude=('song',))


class AlbumUpdate(BaseModel):
    name: str | None
    description: str | None
    is_hidden: bool | None


class AlbumOwner(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    avatar: str | None

    class Config:
        orm_mode = True


class Genre(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class TrackOut(BaseModel):
    id: int
    name: str
    track_author: str
    genre: List[Genre] = []
    song: str
    song_poster: str
    songs_time: str

    class Config:
        orm_mode = True


class AlbumRetrieve(BaseModel):
    id: int
    name: str
    description: str
    poster: str
    band: str
    release_year: str
    owner: AlbumOwner
    is_hidden: bool
    date_created: datetime
    track: List[TrackOut]
    genre: List[Genre]

    class Config:
        orm_mode = True
