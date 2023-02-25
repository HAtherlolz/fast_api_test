from typing import Union, List
from datetime import datetime

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import PlayList

PlayList_Pydantic = pydantic_model_creator(PlayList, name='PlayList')
PlayListIn_Pydantic = pydantic_model_creator(PlayList, name='PlayListIn', exclude_readonly=True)

class PlayListUpdate(BaseModel):
    name: Union[str, None]
    description: Union[str, None]
    is_hidden: bool

class AlbumOwner(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    avatar: str | None

class Genre(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class AlbumRetrieve(BaseModel):
    id: int
    name: str
    description: str
    poster: str
    band: str
    release_year: str
    is_hidden: bool
    date_created: datetime
    genre: List[Genre]

    class Config:
        orm_mode = True

class TrackOut(BaseModel):
    id: int
    name: str
    text: str
    track_author: str
    genre: List[Genre] = []
    album: AlbumRetrieve
    song: str
    song_poster: str
    date_created: datetime


class PlayListOut(BaseModel):
    id: int
    name: str
    description: str
    poster: str
    is_hidden: bool
    owner: AlbumOwner
    track: List[TrackOut] = []
