from tortoise import fields
from tortoise.models import Model

from src.user.models import User
from src.genre.models import Genre
# from src.track.models import Track


class Album(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(25, index=True)
    description = fields.CharField(max_length=1000)
    poster = fields.CharField(max_length=1000)
    band = fields.CharField(max_length=30)
    release_year = fields.CharField(max_length=10)
    owner: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        'models.User', related_name='album', on_delete=fields.CASCADE
    )
    genre: fields.ManyToManyRelation['Genre'] = fields.ManyToManyField(
        'models.Genre', through='album_genre', null=True, related_name='albums'
    )
    is_hidden = fields.BooleanField(default=False)
    views_count = fields.IntField(default=0)
    date_created = fields.DatetimeField(auto_now_add=True)

    class PydanticMeta:
        # exclude = ("owner",)
        pass

    def __str__(self):
        return self.name
