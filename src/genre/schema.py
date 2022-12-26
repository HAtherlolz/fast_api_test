from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Genre

Genre_Pydantic = pydantic_model_creator(Genre, name='Genre', exclude=('password', 'tracks'))
GenreIn_Pydantic = pydantic_model_creator(Genre, name='GenreIn', exclude_readonly=True)


class GenreOut(BaseModel):
    id: int
    name: str