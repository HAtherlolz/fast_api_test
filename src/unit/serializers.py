from typing import Union, List
from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Unit

Unit_Pydantic = pydantic_model_creator(Unit, name='Unit')


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True


class UnitMapIdLAtLngSerializer(OurBaseModel):
    id: int
    lat: Union[float, None]
    lng: Union[float, None]


class ListUnitMapIdLAtLngSerializer(OurBaseModel):
    __root__: List[UnitMapIdLAtLngSerializer]
