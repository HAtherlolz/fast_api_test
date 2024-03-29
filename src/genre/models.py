from tortoise import fields
from tortoise.models import Model


class Genre(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True, index=True)

    def __str__(self):
        return self.name
