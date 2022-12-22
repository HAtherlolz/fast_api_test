from typing import Union
from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import User

User_Pydantic = pydantic_model_creator(User, name='User', exclude=('password',))
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class UserSerializer(BaseModel):
    email: Union[str, None]
    first_name: Union[str, None]
    last_name: Union[str, None]
    is_active: Union[str, None]


class CreateUser(BaseModel):
    email: EmailStr
    password: Union[str, None] = None
