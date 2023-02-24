from tortoise import fields
from tortoise.models import Model

from src.user.models import User
from src.genre.models import Genre
from src.album.models import Album

from .services import delete_file_to_s3


class Track(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    track_author = fields.CharField(max_length=255)
    owner: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        'models.User', related_name='track', on_delete=fields.CASCADE
    )
    genre: fields.ManyToManyRelation['Genre'] = fields.ManyToManyField(
        'models.Genre', through='track_genre', null=True, related_name='tracks'
    )
    album: fields.ForeignKeyRelation['Album'] = fields.ForeignKeyField(
        'models.Album', related_name='track', on_delete=fields.CASCADE, null=True,
    )
    text = fields.TextField()
    date_created = fields.DatetimeField(auto_now_add=True)
    is_hidden = fields.BooleanField(default=False)
    song = fields.CharField(max_length=1000)
    song_poster = fields.CharField(max_length=1000, null=True)
    views_count = fields.IntField(default=0)

    class PydanticMeta:
        exclude = ('views_count',)

    async def delete(self):
        await delete_file_to_s3(self.song_poster)
        await delete_file_to_s3(self.song)
        super.delete()

    def __str__(self):
        return self.name
