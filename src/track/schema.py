from datetime import datetime
from typing import Union, List

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.genre.models import Genre
from .models import Track

Track_Pydantic = pydantic_model_creator(Track, name='Track', exclude=("album__owner",))
TrackIn_Pydantic = pydantic_model_creator(Track, name='TrackIn', exclude_readonly=True, exclude=('song',))

GetGenre = pydantic_model_creator(Genre, name='GetGenre', exclude=('tracks', ))


class TrackUpdate(BaseModel):
    name: Union[str, None]
    track_author: Union[str, None]
    album: Union[int, None]
    text: Union[str, None]
    is_hidden: Union[bool, None]

    class Config:
        orm_mode = True


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


class Album(BaseModel):
    id: int
    name: str
    description: str
    poster: str
    band: str
    release_year: str
    is_hidden: bool
    date_created: datetime

    class Config:
        orm_mode = True


class TrackOut(BaseModel):
    id: int
    name: str
    track_author: str
    owner: AlbumOwner
    genre: List[Genre] = []
    album: Album | None
    text: str | None
    date_created: datetime
    is_hidden: bool
    song: str
    song_poster: str

    class Config:
        orm_mode = True

#
# class TrackCreateForm(BaseModel):
#     name: str
#     track_author: str
#     text: str | None
#     is_hidden: bool
#     album: int | None
#     genre: list[int]
