from datetime import datetime
from typing import Union

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Track

Track_Pydantic = pydantic_model_creator(Track, name='Track')
TrackIn_Pydantic = pydantic_model_creator(Track, name='TrackIn', exclude_readonly=True, exclude=('song',))


class TrackUpdate(BaseModel):
    name: Union[str, None]
    track_author: Union[str, None]
    # genre: list[int] | None
    text: Union[str, None]
    is_hidden: Union[bool, None]

    class Config:
        orm_mode = True
