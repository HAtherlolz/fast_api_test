from typing import Union

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Album

Album_Pydantic = pydantic_model_creator(Album, name='Album')
# AlbumUpdate = pydantic_model_creator(Album, name='AlbumUpdate', exclude=("owner", ))
AlbumIn_Pydantic = pydantic_model_creator(Album, name='AlbumIn', exclude_readonly=True, exclude=('song',))


class AlbumUpdate(BaseModel):
    name: str | None
    description: str | None
    is_hidden: bool | None
