from tortoise import fields
from tortoise.models import Model

from src.user.models import User
# from src.track.models import Track


class Album(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(25, index=True)
    description = fields.CharField(500)
    poster = fields.CharField(300)
    owner: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        'models.User', related_name='album', on_delete=fields.CASCADE
    )
    is_hidden = fields.BooleanField(default=False)
    date_created = fields.DatetimeField(auto_now_add=True)

    class PydanticMeta:
        # exclude = ("owner",)
        pass

    def __str__(self):
        return self.name
