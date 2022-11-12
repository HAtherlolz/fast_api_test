from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Unit

Unit_Pydantic = pydantic_model_creator(Unit, name='User', exclude_readonly=True, exclude=('password',))


class UnitMapIdLAtLngSerializer(BaseModel):
    id: int
    lat: float
    lng: float